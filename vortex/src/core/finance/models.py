"""Database models for the token system.

This module defines the SQLAlchemy models used to store token-related data
in the database. It includes models for balances, transactions, and multipliers,
with appropriate relationships and constraints.

Models:
    TokenBalance: Stores user token balances
    TokenTransactionRecord: Stores transaction history
    TokenMultiplierRecord: Stores active multipliers
"""

from datetime import datetime
from decimal import Decimal
from typing import Dict, Any
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, JSON, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.base import Base
from .token_system import TokenTransactionType

class TokenBalance(Base):
    """Stores user token balances.
    
    This model maintains the current token balance for each user and establishes
    relationships with transaction and multiplier records.
    
    Attributes:
        user_id: Primary key, UUID of the user
        balance: Current token balance with 8 decimal places
        last_updated: Timestamp of last balance update
        transactions: Relationship to transaction records
        multipliers: Relationship to multiplier records
    """
    __tablename__ = 'token_balances'
    
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    balance = Column(Numeric(precision=20, scale=8), nullable=False, default=0)
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    transactions = relationship("TokenTransactionRecord", back_populates="balance")
    multipliers = relationship("TokenMultiplierRecord", back_populates="balance")

class TokenTransactionRecord(Base):
    """Stores token transaction history.
    
    This model maintains a complete history of all token transactions,
    including earnings, spending, and system adjustments.
    
    Attributes:
        transaction_id: Primary key, UUID of the transaction
        user_id: Foreign key to TokenBalance
        transaction_type: Type of transaction from TokenTransactionType
        amount: Transaction amount with 8 decimal places
        timestamp: When the transaction occurred
        description: Human-readable description
        metadata: JSON field for additional data
        balance: Relationship to user's balance record
    """
    __tablename__ = 'token_transactions'
    
    transaction_id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('token_balances.user_id'), nullable=False)
    transaction_type = Column(SQLEnum(TokenTransactionType), nullable=False)
    amount = Column(Numeric(precision=20, scale=8), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String, nullable=False)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    balance = relationship("TokenBalance", back_populates="transactions")

class TokenMultiplierRecord(Base):
    """Stores active token multipliers.
    
    This model tracks active multipliers that affect token earning rates.
    Multipliers can be permanent or temporary with an expiration time.
    
    Attributes:
        id: Primary key, UUID of the multiplier
        user_id: Foreign key to TokenBalance
        name: Identifier for the multiplier
        value: Multiplier value with 4 decimal places
        created_at: When the multiplier was added
        expires_at: When the multiplier expires (null for permanent)
        balance: Relationship to user's balance record
    """
    __tablename__ = 'token_multipliers'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('token_balances.user_id'), nullable=False)
    name = Column(String, nullable=False)
    value = Column(Numeric(precision=10, scale=4), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    balance = relationship("TokenBalance", back_populates="multipliers") 