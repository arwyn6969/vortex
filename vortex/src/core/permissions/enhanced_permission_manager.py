"""Enhanced permission manager for handling complex permission rules."""

from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from uuid import UUID
import logging
from dataclasses import dataclass, field

from .permission_types import (
    UserType,
    PermissionScope,
    ResourceType,
    TimeRestriction
)
from .permission_rule import PermissionRule

logger = logging.getLogger(__name__)

@dataclass
class PermissionState:
    """Tracks the state of a permission for a user."""
    current_uses: int = 0
    last_use_time: Optional[datetime] = None
    concurrent_uses: int = 0

class EnhancedPermissionManager:
    """Manages complex permission rules and checks."""
    
    def __init__(self):
        """Initialize the permission manager."""
        self._rules: Dict[str, PermissionRule] = {}
        self._user_states: Dict[Tuple[UUID, str], PermissionState] = {}
        self._scope_rules: Dict[PermissionScope, List[str]] = {
            scope: [] for scope in PermissionScope
        }
        
    def add_rule(self, rule: PermissionRule) -> bool:
        """Add a new permission rule."""
        if rule.rule_id in self._rules:
            return False
            
        self._rules[rule.rule_id] = rule
        self._scope_rules[rule.scope].append(rule.rule_id)
        # Sort rules by priority within scope
        self._scope_rules[rule.scope].sort(
            key=lambda x: self._rules[x].priority,
            reverse=True
        )
        return True
        
    def update_rule(
        self,
        rule: PermissionRule,
        modifier_id: UUID
    ) -> bool:
        """Update an existing permission rule."""
        if rule.rule_id not in self._rules:
            return False
            
        old_rule = self._rules[rule.rule_id]
        if old_rule.scope != rule.scope:
            # Remove from old scope list
            self._scope_rules[old_rule.scope].remove(rule.rule_id)
            # Add to new scope list
            self._scope_rules[rule.scope].append(rule.rule_id)
            # Resort new scope list
            self._scope_rules[rule.scope].sort(
                key=lambda x: self._rules[x].priority,
                reverse=True
            )
            
        rule.modified_at = datetime.utcnow()
        rule.last_modified_by = modifier_id
        self._rules[rule.rule_id] = rule
        return True
        
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a permission rule."""
        if rule_id not in self._rules:
            return False
            
        rule = self._rules[rule_id]
        self._scope_rules[rule.scope].remove(rule_id)
        del self._rules[rule_id]
        return True
        
    def check_permission(
        self,
        user_id: UUID,
        user_type: UserType,
        scope: PermissionScope,
        action: str,
        zone_id: Optional[str] = None,
        available_resources: Optional[Dict[ResourceType, float]] = None,
        user_achievements: Optional[Set[str]] = None,
        user_items: Optional[Set[str]] = None,
        present_users: Optional[Set[UUID]] = None,
        zone_state: Optional[Dict[str, str]] = None
    ) -> Tuple[bool, Optional[str]]:
        """Check if a user has permission for an action.
        
        Args:
            user_id: The ID of the user
            user_type: The type of user (HUMAN/AI/HYBRID)
            scope: The scope of the permission being checked
            action: The specific action being attempted
            zone_id: Optional zone ID for zone-specific permissions
            available_resources: Optional dict of available resources
            user_achievements: Optional set of user's achievements
            user_items: Optional set of items the user has
            present_users: Optional set of users present in the context
            zone_state: Optional dict of current zone state
            
        Returns:
            Tuple of (has_permission, reason)
        """
        current_time = datetime.utcnow()
        
        # Default empty collections if None
        available_resources = available_resources or {}
        user_achievements = user_achievements or set()
        user_items = user_items or set()
        present_users = present_users or {user_id}
        zone_state = zone_state or {}
        
        # Get relevant rules for the scope
        relevant_rules = []
        for rule_id in self._scope_rules[scope]:
            rule = self._rules[rule_id]
            if not rule.is_active:
                continue
                
            # Check basic scope requirements
            if scope == PermissionScope.ZONE and zone_id not in (rule.zone_ids or {}):
                continue
            if scope == PermissionScope.API and action not in (rule.api_endpoints or {}):
                continue
            if scope == PermissionScope.SPELL and action not in (rule.spell_types or {}):
                continue
            if scope == PermissionScope.ITEM and action not in (rule.item_types or {}):
                continue
            if scope == PermissionScope.CREATION and action not in (rule.creation_types or {}):
                continue
                
            relevant_rules.append(rule)
            
        # No rules found
        if not relevant_rules:
            return False, "No applicable permission rules found"
            
        # Check each rule in priority order
        for rule in relevant_rules:
            # Check user type
            if user_type not in rule.allowed_user_types:
                continue
                
            # Get or create permission state
            state_key = (user_id, rule.rule_id)
            if state_key not in self._user_states:
                self._user_states[state_key] = PermissionState()
            state = self._user_states[state_key]
            
            # Check time restrictions
            if not rule.check_time_restriction(current_time):
                continue
                
            # Check resource requirements
            if not rule.check_resource_requirements(available_resources):
                continue
                
            # Check contextual conditions
            if not rule.check_contextual_conditions(
                user_type,
                user_achievements,
                user_items,
                present_users,
                zone_state
            ):
                continue
                
            # Check usage limits
            if not rule.check_usage_limits(
                state.current_uses,
                state.last_use_time,
                current_time,
                state.concurrent_uses
            ):
                continue
                
            # All checks passed - permission granted
            return True, None
            
        return False, "No matching permission rules allow this action"
        
    def record_usage(
        self,
        user_id: UUID,
        rule_id: str
    ) -> None:
        """Record the usage of a permission rule by a user."""
        if rule_id not in self._rules:
            return
            
        state_key = (user_id, rule_id)
        if state_key not in self._user_states:
            self._user_states[state_key] = PermissionState()
            
        state = self._user_states[state_key]
        state.current_uses += 1
        state.last_use_time = datetime.utcnow()
        state.concurrent_uses += 1
        
    def release_usage(
        self,
        user_id: UUID,
        rule_id: str
    ) -> None:
        """Release a concurrent usage of a permission rule."""
        state_key = (user_id, rule_id)
        if state_key in self._user_states:
            self._user_states[state_key].concurrent_uses = max(
                0,
                self._user_states[state_key].concurrent_uses - 1
            )
            
    def get_available_actions(
        self,
        user_id: UUID,
        user_type: UserType,
        scope: PermissionScope,
        zone_id: Optional[str] = None,
        available_resources: Optional[Dict[ResourceType, float]] = None,
        user_achievements: Optional[Set[str]] = None,
        user_items: Optional[Set[str]] = None,
        present_users: Optional[Set[UUID]] = None,
        zone_state: Optional[Dict[str, str]] = None
    ) -> Set[str]:
        """Get all actions available to a user in the given context."""
        available_actions = set()
        
        for rule in self._rules.values():
            if rule.scope != scope or not rule.is_active:
                continue
                
            # Get potential actions based on scope
            potential_actions = set()
            if scope == PermissionScope.ZONE and zone_id in (rule.zone_ids or {}):
                potential_actions.update(rule.zone_ids or {})
            elif scope == PermissionScope.API:
                potential_actions.update(rule.api_endpoints or {})
            elif scope == PermissionScope.SPELL:
                potential_actions.update(rule.spell_types or {})
            elif scope == PermissionScope.ITEM:
                potential_actions.update(rule.item_types or {})
            elif scope == PermissionScope.CREATION:
                potential_actions.update(rule.creation_types or {})
                
            # Check each potential action
            for action in potential_actions:
                has_permission, _ = self.check_permission(
                    user_id,
                    user_type,
                    scope,
                    action,
                    zone_id,
                    available_resources,
                    user_achievements,
                    user_items,
                    present_users,
                    zone_state
                )
                if has_permission:
                    available_actions.add(action)
                    
        return available_actions 