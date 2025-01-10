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
    - Bitcoin token support (STAMPS and SRC-20)
    - Special token multipliers

Classes:
    TokenService: Main service class for token management
"""

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4
import asyncio

from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from .models import TokenBalance, TokenTransactionRecord, TokenMultiplierRecord, BitcoinTokenRecord
from .token_system import TokenTransactionType, TokenTransaction
from .bitcoin_tokens import BitcoinTokenService, BitcoinTokenBalance, BitcoinTokenType
from .token_config import calculate_token_multipliers
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
        bitcoin_service: Service for Bitcoin token operations
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
        self.bitcoin_service = BitcoinTokenService()
        
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
        
    async def _get_special_token_multiplier(self, user_id: UUID) -> Decimal:
        """Calculate multiplier from special tokens owned by user.
        
        This includes both STAMPS and SRC-20 tokens that provide multipliers.
        The multipliers are stackable and add to the base multiplier.
        
        Args:
            user_id: User to calculate multiplier for
            
        Returns:
            Total multiplier from special tokens
        """
        # Get all user's Bitcoin tokens
        bitcoin_tokens = await self.get_bitcoin_token_balances(user_id)
        
        # Extract owned token IDs
        src20_tokens: Set[str] = set()
        stamps: Set[str] = set()
        
        for token in bitcoin_tokens:
            if token.balance > 0:
                if token.token_type == BitcoinTokenType.SRC20:
                    src20_tokens.add(token.token_id)
                else:  # STAMPS
                    stamps.add(token.token_id)
        
        # Calculate total multiplier
        return calculate_token_multipliers(src20_tokens, stamps)
    
    def _get_current_multiplier(self, user_id: UUID) -> Decimal:
        """Calculate current total multiplier for user.
        
        This method retrieves all active multipliers for a user and
        calculates their combined effect. This includes:
        - Base multiplier (1.0)
        - Active time-based multipliers
        - Special token multipliers (STAMPS and SRC-20)
        
        Args:
            user_id: ID of the user
        
        Returns:
            The product of all active multipliers
        """
        now = datetime.utcnow()
        
        # Get active time-based multipliers
        multipliers = self.db.query(TokenMultiplierRecord).filter(
            and_(
                TokenMultiplierRecord.user_id == user_id,
                TokenMultiplierRecord.expires_at.is_(None) | 
                (TokenMultiplierRecord.expires_at > now)
            )
        ).all()
        
        # Calculate total time-based multiplier
        total = Decimal('1.0')
        for multiplier in multipliers:
            total *= multiplier.value
        
        # Add special token multipliers
        special_multiplier = asyncio.run(self._get_special_token_multiplier(user_id))
        total *= special_multiplier
        
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
        
    async def get_bitcoin_token_balances(
        self,
        user_id: UUID,
        token_type: Optional[BitcoinTokenType] = None,
        token_id: Optional[str] = None,
        force_refresh: bool = False
    ) -> List[BitcoinTokenBalance]:
        """Get Bitcoin token balances for a user.
        
        Args:
            user_id: User to get balances for
            token_type: Optional filter by token type
            token_id: Optional filter by token ID
            force_refresh: Whether to force a refresh from the API
            
        Returns:
            List of token balances
        """
        # Get user's Bitcoin address
        balance = self.db.query(TokenBalance).filter(
            TokenBalance.user_id == user_id
        ).first()
        
        if not balance or not balance.bitcoin_address:
            return []
            
        # Check if we need to refresh from API
        query = self.db.query(BitcoinTokenRecord).filter(
            BitcoinTokenRecord.user_id == user_id
        )
        
        if token_type:
            query = query.filter(BitcoinTokenRecord.token_type == token_type.name)
        if token_id:
            query = query.filter(BitcoinTokenRecord.token_id == token_id)
            
        existing = query.all()
        
        # If force refresh or no existing records, fetch from API
        if force_refresh or not existing:
            balances = await self.bitcoin_service.get_combined_balances(
                balance.bitcoin_address
            )
            
            # Update database records
            for token_balance in balances:
                record = self.db.query(BitcoinTokenRecord).filter(
                    and_(
                        BitcoinTokenRecord.user_id == user_id,
                        BitcoinTokenRecord.token_type == token_balance.token_type.name,
                        BitcoinTokenRecord.token_id == token_balance.token_id
                    )
                ).first()
                
                if record:
                    record.balance = token_balance.balance
                    record.last_updated = token_balance.last_updated
                    record.metadata = token_balance.metadata
                else:
                    record = BitcoinTokenRecord(
                        user_id=user_id,
                        token_type=token_balance.token_type.name,
                        token_id=token_balance.token_id,
                        balance=token_balance.balance,
                        last_updated=token_balance.last_updated,
                        metadata=token_balance.metadata
                    )
                    self.db.add(record)
                    
            self.db.commit()
            return balances
            
        # Convert database records to BitcoinTokenBalance objects
        return [
            BitcoinTokenBalance(
                token_type=BitcoinTokenType[record.token_type],
                token_id=record.token_id,
                balance=record.balance,
                last_updated=record.last_updated,
                metadata=record.metadata or {}
            )
            for record in existing
        ]
        
    async def close(self):
        """Close any open connections."""
        await self.bitcoin_service.close() 