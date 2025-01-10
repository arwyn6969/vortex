"""Permission types and conditions for the enhanced permission system."""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Union
from datetime import datetime, time
from uuid import UUID

class UserType(Enum):
    """Types of users in the system."""
    HUMAN = auto()
    AI = auto()
    HYBRID = auto()  # For systems that combine both

class PermissionScope(Enum):
    """Scopes where permissions can be applied."""
    GLOBAL = auto()  # Applies everywhere
    ZONE = auto()   # Specific to a zone/room
    INTERACTION = auto()  # During specific interactions
    ITEM = auto()   # Related to item usage
    API = auto()    # API access
    SPELL = auto()  # Spell casting
    CREATION = auto()  # Content creation

class ResourceType(Enum):
    """Types of resources that can be required for permissions."""
    TOKENS = auto()
    CREDITS = auto()
    ENERGY = auto()
    MANA = auto()
    REPUTATION = auto()
    ACHIEVEMENT_POINTS = auto()

class TimeRestriction(Enum):
    """Types of time-based restrictions."""
    ALWAYS = auto()
    DAILY = auto()
    WEEKLY = auto()
    MONTHLY = auto()
    CUSTOM = auto()

@dataclass
class TimeWindow:
    """Represents a time window when a permission is valid."""
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    days_of_week: Set[int] = None  # 0=Monday, 6=Sunday
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

@dataclass
class ResourceRequirement:
    """Resource requirements for a permission."""
    resource_type: ResourceType
    amount: float
    is_consumed: bool = False  # Whether the resource is consumed on use
    replenish_rate: Optional[float] = None  # Amount replenished per hour

@dataclass
class ContextualCondition:
    """Contextual conditions for permission validity."""
    required_user_types: Optional[Set[UserType]] = None
    required_achievements: Optional[Set[str]] = None
    required_items: Optional[Set[str]] = None
    excluded_users: Optional[Set[UUID]] = None
    required_users: Optional[Set[UUID]] = None
    min_user_count: Optional[int] = None
    max_user_count: Optional[int] = None
    required_zone_states: Optional[Dict[str, str]] = None

@dataclass
class UsageLimit:
    """Limits on permission usage."""
    max_uses: Optional[int] = None
    cooldown_seconds: Optional[int] = None
    rate_limit_period: Optional[int] = None  # In seconds
    rate_limit_count: Optional[int] = None
    concurrent_use_limit: Optional[int] = None 