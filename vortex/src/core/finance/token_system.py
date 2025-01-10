"""Token system for tracking and managing user tokens.

This module implements a hidden token economy system that rewards players for their
interactions within the game. The system remains hidden until players accumulate
enough tokens to discover it.

Key Features:
    - Hidden token earning through keystrokes
    - Multiplier system for bonus earnings
    - Achievement integration
    - Transaction history tracking
    - Balance management with security features

Classes:
    TokenTransactionType: Enum for different types of token transactions
    TokenTransaction: Dataclass representing a single token transaction
    TokenMultiplier: Class managing token earning multipliers
    TokenSystem: Main token management system
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional
from uuid import UUID
import json
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class TokenTransactionType(Enum):
    """Types of token transactions.
    
    Attributes:
        KEYSTROKE: Tokens earned from keystrokes
        CHALLENGE: Tokens earned from completing challenges
        MULTIPLIER: Tokens earned from multiplier events
        PURCHASE: Tokens purchased by the user
        SPEND: Tokens spent on services
        SYSTEM: System-level token adjustments
    """
    KEYSTROKE = auto()  # Earned from keystrokes
    CHALLENGE = auto()  # Earned from completing challenges
    MULTIPLIER = auto()  # Earned from multiplier events
    PURCHASE = auto()  # Tokens purchased
    SPEND = auto()  # Tokens spent on services
    SYSTEM = auto()  # System-level adjustments

@dataclass
class TokenTransaction:
    """Represents a single token transaction.
    
    Attributes:
        transaction_id: Unique identifier for the transaction
        user_id: ID of the user involved in the transaction
        transaction_type: Type of transaction from TokenTransactionType
        amount: Amount of tokens involved (positive for earning, negative for spending)
        timestamp: When the transaction occurred
        description: Human-readable description of the transaction
        metadata: Additional transaction data as key-value pairs
    """
    transaction_id: UUID
    user_id: UUID
    transaction_type: TokenTransactionType
    amount: Decimal
    timestamp: datetime
    description: str
    metadata: Dict = None

class TokenMultiplier:
    """Manages token earning multipliers.
    
    This class handles temporary and permanent multipliers that affect token
    earning rates. Multipliers stack multiplicatively.
    
    Attributes:
        base_multiplier: Default multiplier value (1.0)
        temporary_multipliers: Dict of named multipliers and their values
        expiry_times: Dict tracking when temporary multipliers expire
    """
    
    def __init__(self):
        """Initialize a new token multiplier manager."""
        self.base_multiplier: Decimal = Decimal('1.0')
        self.temporary_multipliers: Dict[str, Decimal] = {}
        self.expiry_times: Dict[str, datetime] = {}
    
    def add_multiplier(self, name: str, value: Decimal, duration_seconds: int = None):
        """Add a temporary multiplier.
        
        Args:
            name: Unique identifier for the multiplier
            value: Multiplier value (e.g., 1.5 for 50% bonus)
            duration_seconds: Optional duration after which multiplier expires
        """
        self.temporary_multipliers[name] = value
        if duration_seconds:
            self.expiry_times[name] = datetime.utcnow().timestamp() + duration_seconds
    
    def remove_multiplier(self, name: str):
        """Remove a temporary multiplier.
        
        Args:
            name: Identifier of the multiplier to remove
        """
        self.temporary_multipliers.pop(name, None)
        self.expiry_times.pop(name, None)
    
    def get_current_multiplier(self) -> Decimal:
        """Calculate current total multiplier.
        
        Returns:
            The product of all active multipliers
        """
        now = datetime.utcnow().timestamp()
        
        # Remove expired multipliers
        expired = [name for name, expiry in self.expiry_times.items() 
                  if expiry <= now]
        for name in expired:
            self.remove_multiplier(name)
        
        # Calculate total multiplier
        total = self.base_multiplier
        for multiplier in self.temporary_multipliers.values():
            total *= multiplier
        return total

class TokenSystem:
    """Main token management system.
    
    This class handles all token-related operations including earning,
    spending, and multiplier management. It includes rate limiting and
    security features to prevent abuse.
    
    Attributes:
        balances: Dict mapping user IDs to token balances
        transactions: List of all token transactions
        multipliers: Dict mapping user IDs to their TokenMultiplier
        keystroke_rate: Base rate of tokens earned per keystroke
        token_visibility_threshold: Balance required to reveal system
    """
    
    def __init__(self):
        """Initialize the token system."""
        self.balances: Dict[UUID, Decimal] = {}
        self.transactions: List[TokenTransaction] = []
        self.multipliers: Dict[UUID, TokenMultiplier] = {}
        self.keystroke_rate = Decimal('0.001')  # Base rate per keystroke
        self.token_visibility_threshold = Decimal('100.0')  # When tokens become visible
        
    def get_balance(self, user_id: UUID, include_hidden: bool = False) -> Optional[Decimal]:
        """Get user's token balance.
        
        Args:
            user_id: ID of the user
            include_hidden: Whether to show balance below visibility threshold
        
        Returns:
            Current balance or None if hidden
        """
        balance = self.balances.get(user_id, Decimal('0.0'))
        if not include_hidden and balance < self.token_visibility_threshold:
            return None
        return balance
    
    def add_transaction(self, 
                       user_id: UUID, 
                       amount: Decimal,
                       transaction_type: TokenTransactionType,
                       description: str,
                       metadata: Dict = None) -> TokenTransaction:
        """Record a new transaction.
        
        Args:
            user_id: ID of the user
            amount: Amount of tokens (positive for earning, negative for spending)
            transaction_type: Type of transaction
            description: Human-readable description
            metadata: Additional transaction data
        
        Returns:
            The created transaction record
        """
        from uuid import uuid4
        
        transaction = TokenTransaction(
            transaction_id=uuid4(),
            user_id=user_id,
            transaction_type=transaction_type,
            amount=amount,
            timestamp=datetime.utcnow(),
            description=description,
            metadata=metadata or {}
        )
        
        # Update balance
        if user_id not in self.balances:
            self.balances[user_id] = Decimal('0.0')
        self.balances[user_id] += amount
        
        # Record transaction
        self.transactions.append(transaction)
        
        # Log transaction
        logger.info(f"Token transaction: {user_id} {transaction_type.name} {amount}")
        
        return transaction
    
    def record_keystrokes(self, user_id: UUID, keystroke_count: int):
        """Record keystrokes and award tokens.
        
        Args:
            user_id: ID of the user
            keystroke_count: Number of keystrokes to record
        
        Returns:
            The created transaction record
        """
        if user_id not in self.multipliers:
            self.multipliers[user_id] = TokenMultiplier()
        
        multiplier = self.multipliers[user_id].get_current_multiplier()
        amount = Decimal(str(keystroke_count)) * self.keystroke_rate * multiplier
        
        return self.add_transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=TokenTransactionType.KEYSTROKE,
            description=f"Earned from {keystroke_count} keystrokes",
            metadata={"keystroke_count": keystroke_count, "multiplier": float(multiplier)}
        )
    
    def add_multiplier(self, user_id: UUID, name: str, value: Decimal, duration_seconds: int = None):
        """Add a token earning multiplier for a user.
        
        Args:
            user_id: ID of the user
            name: Unique identifier for the multiplier
            value: Multiplier value (e.g., 1.5 for 50% bonus)
            duration_seconds: Optional duration after which multiplier expires
        """
        if user_id not in self.multipliers:
            self.multipliers[user_id] = TokenMultiplier()
        self.multipliers[user_id].add_multiplier(name, value, duration_seconds)
    
    def get_transaction_history(self, 
                              user_id: UUID, 
                              include_hidden: bool = False,
                              limit: int = 50) -> List[TokenTransaction]:
        """Get user's transaction history.
        
        Args:
            user_id: ID of the user
            include_hidden: Whether to show history when balance is hidden
            limit: Maximum number of transactions to return
        
        Returns:
            List of transactions, newest first
        """
        if not include_hidden and self.get_balance(user_id) is None:
            return []
        
        user_transactions = [t for t in self.transactions 
                           if t.user_id == user_id]
        return sorted(user_transactions, 
                     key=lambda x: x.timestamp, 
                     reverse=True)[:limit]
    
    def can_spend(self, user_id: UUID, amount: Decimal) -> bool:
        """Check if user has sufficient tokens to spend.
        
        Args:
            user_id: ID of the user
            amount: Amount of tokens to check
        
        Returns:
            True if user can spend the amount
        """
        balance = self.balances.get(user_id, Decimal('0.0'))
        return balance >= amount
    
    def spend_tokens(self, 
                    user_id: UUID, 
                    amount: Decimal, 
                    description: str,
                    metadata: Dict = None) -> Optional[TokenTransaction]:
        """Spend tokens if user has sufficient balance.
        
        Args:
            user_id: ID of the user
            amount: Amount of tokens to spend
            description: Purpose of the spending
            metadata: Additional transaction data
        
        Returns:
            Transaction record if successful, None if insufficient balance
        """
        if not self.can_spend(user_id, amount):
            return None
        
        return self.add_transaction(
            user_id=user_id,
            amount=-amount,  # Negative for spending
            transaction_type=TokenTransactionType.SPEND,
            description=description,
            metadata=metadata
        ) 