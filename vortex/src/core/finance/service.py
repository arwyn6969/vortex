"""Service layer for the token system.

This module provides a high-level interface for token management, handling database
operations, achievement tracking, and security features. It implements rate limiting,
transaction locking, and other safeguards to ensure system integrity.

Key Features:
    - Database-backed token storage
    - Achievement integration
    - Rate limiting and security
    - Transaction history
    - Multiplier management

Classes:
    TokenService: Main service class for token management
"""

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from .models import TokenBalance, TokenTransactionRecord, TokenMultiplierRecord
from .token_system import TokenTransactionType, TokenTransaction
from ..achievements import AchievementManager
from ..db.session import get_db

class TokenService:
    """Service for managing the token system.
    
    This class provides a high-level interface for token operations, handling
    database persistence, achievement tracking, and security features. It includes
    rate limiting for token generation and transaction locks for data integrity.
    
    Attributes:
        db: SQLAlchemy database session
        achievement_manager: Achievement system integration
        keystroke_rate: Base rate of tokens per keystroke
        token_visibility_threshold: Balance required to reveal system
        max_keystrokes_per_minute: Rate limit for keystroke tracking
        keystroke_cooldowns: Rate limiting state storage
    """
    
    def __init__(self, db: Session, achievement_manager: AchievementManager):
        """Initialize the token service.
        
        Args:
            db: SQLAlchemy database session
            achievement_manager: Achievement system for tracking progress
        """
        self.db = db
        self.achievement_manager = achievement_manager
        self.keystroke_rate = Decimal('0.001')  # Base rate per keystroke
        self.token_visibility_threshold = Decimal('100.0')
        self.max_keystrokes_per_minute = 300  # Reasonable typing speed limit
        self.keystroke_cooldowns = {}  # Track last keystroke time per user
        
    def get_balance(self, user_id: UUID, include_hidden: bool = False) -> Optional[Decimal]:
        """Get user's token balance.
        
        Args:
            user_id: ID of the user
            include_hidden: Whether to show balance below visibility threshold
        
        Returns:
            Current balance or None if hidden
        """
        balance = self.db.query(TokenBalance).filter(
            TokenBalance.user_id == user_id
        ).first()
        
        if not balance:
            return Decimal('0.0')
            
        if not include_hidden and balance.balance < self.token_visibility_threshold:
            return None
            
        return balance.balance
        
    def record_keystrokes(self, user_id: UUID, keystroke_count: int) -> TokenTransactionRecord:
        """Record keystrokes and award tokens.
        
        This method includes rate limiting to prevent abuse. It tracks the time
        between keystroke batches and limits the maximum number of keystrokes
        that can be processed per minute.
        
        Args:
            user_id: ID of the user
            keystroke_count: Number of keystrokes to record
        
        Returns:
            The created transaction record
        """
        now = datetime.utcnow()
        last_keystroke = self.keystroke_cooldowns.get(user_id)
        
        # Apply rate limiting
        if last_keystroke:
            time_diff = (now - last_keystroke).total_seconds()
            max_keystrokes = (time_diff / 60.0) * self.max_keystrokes_per_minute
            keystroke_count = min(keystroke_count, int(max_keystrokes))
            
        if keystroke_count <= 0:
            return None
            
        self.keystroke_cooldowns[user_id] = now
        
        # Get current multiplier
        multiplier = self._get_current_multiplier(user_id)
        amount = Decimal(str(keystroke_count)) * self.keystroke_rate * multiplier
        
        # Create transaction
        transaction = self._create_transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=TokenTransactionType.KEYSTROKE,
            description=f"Earned from {keystroke_count} keystrokes",
            metadata={"keystroke_count": keystroke_count, "multiplier": float(multiplier)}
        )
        
        # Check for token-related achievements
        self._check_token_achievements(user_id)
        
        return transaction
        
    def add_multiplier(self, 
                      user_id: UUID, 
                      name: str, 
                      value: Decimal, 
                      duration_seconds: Optional[int] = None) -> TokenMultiplierRecord:
        """Add a token earning multiplier for a user."""
        expires_at = None
        if duration_seconds:
            expires_at = datetime.utcnow().timestamp() + duration_seconds
            
        multiplier = TokenMultiplierRecord(
            id=uuid4(),
            user_id=user_id,
            name=name,
            value=value,
            expires_at=expires_at
        )
        
        self.db.add(multiplier)
        self.db.commit()
        
        return multiplier
        
    def get_transaction_history(self,
                              user_id: UUID,
                              include_hidden: bool = False,
                              limit: int = 50) -> List[TokenTransactionRecord]:
        """Get user's transaction history."""
        if not include_hidden and self.get_balance(user_id) is None:
            return []
            
        query = select(TokenTransactionRecord).filter(
            TokenTransactionRecord.user_id == user_id
        ).order_by(
            TokenTransactionRecord.timestamp.desc()
        ).limit(limit)
        
        return list(self.db.execute(query).scalars())
        
    def spend_tokens(self,
                    user_id: UUID,
                    amount: Decimal,
                    description: str,
                    metadata: Dict = None) -> Optional[TokenTransactionRecord]:
        """Spend tokens if user has sufficient balance.
        
        This method uses transaction locks to ensure atomicity and prevent
        race conditions when spending tokens.
        
        Args:
            user_id: ID of the user
            amount: Amount of tokens to spend
            description: Purpose of the spending
            metadata: Additional transaction data
        
        Returns:
            Transaction record if successful, None if insufficient balance
        
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
            
        balance = self.get_balance(user_id, include_hidden=True)
        if balance < amount:
            return None
            
        # Ensure transaction won't result in negative balance
        with self.db.begin_nested():
            current_balance = self.db.query(TokenBalance).filter(
                TokenBalance.user_id == user_id
            ).with_for_update().first()
            
            if not current_balance or current_balance.balance < amount:
                return None
                
            return self._create_transaction(
                user_id=user_id,
                amount=-amount,  # Negative for spending
                transaction_type=TokenTransactionType.SPEND,
                description=description,
                metadata=metadata
            )
        
    def _create_transaction(self,
                          user_id: UUID,
                          amount: Decimal,
                          transaction_type: TokenTransactionType,
                          description: str,
                          metadata: Dict = None) -> TokenTransactionRecord:
        """Create and record a new transaction.
        
        This method handles the atomic creation of transactions and balance
        updates, using database locks to prevent race conditions.
        
        Args:
            user_id: ID of the user
            amount: Amount of tokens (positive for earning, negative for spending)
            transaction_type: Type of transaction
            description: Human-readable description
            metadata: Additional transaction data
        
        Returns:
            The created transaction record
        """
        # Get or create balance record with transaction lock
        with self.db.begin_nested():
            balance = self.db.query(TokenBalance).filter(
                TokenBalance.user_id == user_id
            ).with_for_update().first()
            
            if not balance:
                balance = TokenBalance(user_id=user_id, balance=Decimal('0.0'))
                self.db.add(balance)
                
            # Create transaction record
            transaction = TokenTransactionRecord(
                transaction_id=uuid4(),
                user_id=user_id,
                transaction_type=transaction_type,
                amount=amount,
                description=description,
                metadata=metadata or {}
            )
            
            # Update balance
            balance.balance += amount
            balance.last_updated = datetime.utcnow()
            
            # Save changes
            self.db.add(transaction)
            self.db.commit()
            
            return transaction
        
    def _get_current_multiplier(self, user_id: UUID) -> Decimal:
        """Calculate current total multiplier for user.
        
        This method retrieves all active multipliers for a user and
        calculates their combined effect. Expired multipliers are
        automatically filtered out.
        
        Args:
            user_id: ID of the user
        
        Returns:
            The product of all active multipliers
        """
        now = datetime.utcnow()
        
        # Get active multipliers
        multipliers = self.db.query(TokenMultiplierRecord).filter(
            and_(
                TokenMultiplierRecord.user_id == user_id,
                TokenMultiplierRecord.expires_at.is_(None) | 
                (TokenMultiplierRecord.expires_at > now)
            )
        ).all()
        
        # Calculate total multiplier
        total = Decimal('1.0')
        for multiplier in multipliers:
            total *= multiplier.value
            
        return total
        
    def _check_token_achievements(self, user_id: UUID):
        """Check and award any token-related achievements.
        
        This method checks various token-related milestones and awards
        achievements when appropriate.
        
        Args:
            user_id: ID of the user
        """
        balance = self.get_balance(user_id, include_hidden=True)
        
        # Example achievement checks
        if balance >= self.token_visibility_threshold:
            self.achievement_manager.award_achievement(
                user_id, 
                "token_discovery",  # Achievement ID
                {"balance": float(balance)}
            )
            
        # Add more achievement checks as needed
        milestone_amounts = [1000, 10000, 100000]
        for amount in milestone_amounts:
            if balance >= amount:
                self.achievement_manager.award_achievement(
                    user_id,
                    f"token_milestone_{amount}",
                    {"balance": float(balance)}
                ) 