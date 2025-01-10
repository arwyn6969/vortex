"""Permission system for managing access control in Vortex."""

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
from .permission_rule import PermissionRule
from .enhanced_permission_manager import EnhancedPermissionManager, PermissionState

# Re-export from legacy system for backward compatibility
from .legacy import Permission, Role, PermissionManager

__all__ = [
    # Enhanced permission system
    'UserType',
    'PermissionScope',
    'ResourceType',
    'TimeRestriction',
    'TimeWindow',
    'ResourceRequirement',
    'ContextualCondition',
    'UsageLimit',
    'PermissionRule',
    'EnhancedPermissionManager',
    'PermissionState',
    
    # Legacy system
    'Permission',
    'Role',
    'PermissionManager'
] 