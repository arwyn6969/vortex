"""Permission rule system for managing complex permission conditions."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Union
from datetime import datetime
from uuid import UUID

from .permission_types import (
    UserType,
    PermissionScope,
    ResourceType,
    TimeRestriction,
    TimeWindow,
    ResourceRequirement,
    ContextualCondition,
    UsageLimit
)

@dataclass
class PermissionRule:
    """Represents a complete permission rule with all conditions."""
    rule_id: str
    name: str
    description: str
    scope: PermissionScope
    allowed_user_types: Set[UserType]
    
    # Core permission attributes
    is_active: bool = True
    priority: int = 0  # Higher priority rules override lower ones
    
    # Scope-specific attributes
    zone_ids: Optional[Set[str]] = None  # For ZONE scope
    api_endpoints: Optional[Set[str]] = None  # For API scope
    spell_types: Optional[Set[str]] = None  # For SPELL scope
    item_types: Optional[Set[str]] = None  # For ITEM scope
    creation_types: Optional[Set[str]] = None  # For CREATION scope
    
    # Time restrictions
    time_restriction: TimeRestriction = TimeRestriction.ALWAYS
    time_windows: List[TimeWindow] = field(default_factory=list)
    
    # Resource requirements
    resource_requirements: List[ResourceRequirement] = field(default_factory=list)
    
    # Contextual conditions
    contextual_conditions: Optional[ContextualCondition] = None
    
    # Usage limits
    usage_limits: Optional[UsageLimit] = None
    
    # Tracking fields
    created_at: datetime = field(default_factory=datetime.utcnow)
    modified_at: datetime = field(default_factory=datetime.utcnow)
    created_by: Optional[UUID] = None
    last_modified_by: Optional[UUID] = None

    def check_time_restriction(self, current_time: datetime) -> bool:
        """Check if the permission is valid at the given time."""
        if self.time_restriction == TimeRestriction.ALWAYS:
            return True
            
        if not self.time_windows:
            return True
            
        for window in self.time_windows:
            # Check absolute validity period
            if window.valid_from and current_time < window.valid_from:
                continue
            if window.valid_until and current_time > window.valid_until:
                continue
                
            # Check day of week
            if window.days_of_week and current_time.weekday() not in window.days_of_week:
                continue
                
            # Check time of day
            current_time_of_day = current_time.time()
            if window.start_time and current_time_of_day < window.start_time:
                continue
            if window.end_time and current_time_of_day > window.end_time:
                continue
                
            return True
            
        return False
        
    def check_resource_requirements(
        self,
        available_resources: Dict[ResourceType, float]
    ) -> bool:
        """Check if all resource requirements are met."""
        for req in self.resource_requirements:
            if req.resource_type not in available_resources:
                return False
            if available_resources[req.resource_type] < req.amount:
                return False
        return True
        
    def check_contextual_conditions(
        self,
        user_type: UserType,
        user_achievements: Set[str],
        user_items: Set[str],
        present_users: Set[UUID],
        zone_state: Dict[str, str]
    ) -> bool:
        """Check if all contextual conditions are met."""
        if not self.contextual_conditions:
            return True
            
        cond = self.contextual_conditions
        
        # Check user type requirements
        if (cond.required_user_types and 
            user_type not in cond.required_user_types):
            return False
            
        # Check achievement requirements
        if (cond.required_achievements and 
            not cond.required_achievements.issubset(user_achievements)):
            return False
            
        # Check item requirements
        if (cond.required_items and 
            not cond.required_items.issubset(user_items)):
            return False
            
        # Check user presence requirements
        if cond.excluded_users and present_users.intersection(cond.excluded_users):
            return False
        if (cond.required_users and 
            not cond.required_users.issubset(present_users)):
            return False
            
        # Check user count requirements
        present_count = len(present_users)
        if cond.min_user_count and present_count < cond.min_user_count:
            return False
        if cond.max_user_count and present_count > cond.max_user_count:
            return False
            
        # Check zone state requirements
        if cond.required_zone_states:
            for key, value in cond.required_zone_states.items():
                if zone_state.get(key) != value:
                    return False
                    
        return True
        
    def check_usage_limits(
        self,
        current_uses: int,
        last_use_time: Optional[datetime],
        current_time: datetime,
        concurrent_uses: int
    ) -> bool:
        """Check if usage limits allow another use."""
        if not self.usage_limits:
            return True
            
        limits = self.usage_limits
        
        # Check max uses
        if limits.max_uses and current_uses >= limits.max_uses:
            return False
            
        # Check cooldown
        if (limits.cooldown_seconds and last_use_time and
            (current_time - last_use_time).total_seconds() < limits.cooldown_seconds):
            return False
            
        # Check rate limit
        if limits.rate_limit_period and limits.rate_limit_count:
            # This would need to be implemented with a proper rate limiting system
            pass
            
        # Check concurrent use limit
        if (limits.concurrent_use_limit and 
            concurrent_uses >= limits.concurrent_use_limit):
            return False
            
        return True 