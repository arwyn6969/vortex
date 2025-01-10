"""Legacy permission system for backward compatibility."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Set
from uuid import UUID

class Permission(Enum):
    """Available permissions in the system."""
    CREATE_ITEM = auto()
    MODIFY_ITEM = auto()
    DELETE_ITEM = auto()
    CREATE_SCENE = auto()
    MODIFY_SCENE = auto()
    DELETE_SCENE = auto()
    CREATE_CHARACTER = auto()
    MODIFY_CHARACTER = auto()
    DELETE_CHARACTER = auto()
    ADMIN = auto()  # Grants all permissions

@dataclass
class Role:
    """Represents a role with associated permissions."""
    name: str
    permissions: Set[Permission]
    can_grant: Set[Permission]  # Permissions this role can grant to others

class PermissionManager:
    """Manages user permissions and roles."""
    
    def __init__(self):
        self._user_roles: Dict[UUID, Set[str]] = {}
        self._roles: Dict[str, Role] = {}
        self._initialize_default_roles()
    
    def _initialize_default_roles(self):
        """Initialize default system roles."""
        # Admin role
        self._roles["admin"] = Role(
            name="admin",
            permissions=set(Permission),
            can_grant=set(Permission)
        )
        
        # Content Creator role
        creator_permissions = {
            Permission.CREATE_ITEM,
            Permission.MODIFY_ITEM,
            Permission.CREATE_SCENE,
            Permission.MODIFY_SCENE,
            Permission.CREATE_CHARACTER,
            Permission.MODIFY_CHARACTER
        }
        self._roles["content_creator"] = Role(
            name="content_creator",
            permissions=creator_permissions,
            can_grant=set()  # Cannot grant permissions
        )
        
        # Moderator role
        moderator_permissions = {
            Permission.MODIFY_ITEM,
            Permission.DELETE_ITEM,
            Permission.MODIFY_SCENE,
            Permission.DELETE_SCENE,
            Permission.MODIFY_CHARACTER,
            Permission.DELETE_CHARACTER
        }
        self._roles["moderator"] = Role(
            name="moderator",
            permissions=moderator_permissions,
            can_grant=set()
        )
        
    def create_role(
        self,
        role_name: str,
        permissions: Set[Permission],
        can_grant: Set[Permission],
        creator_id: UUID
    ) -> bool:
        """Create a new role."""
        if not self.has_permission(creator_id, Permission.ADMIN):
            return False
            
        if role_name in self._roles:
            return False
            
        self._roles[role_name] = Role(
            name=role_name,
            permissions=permissions,
            can_grant=can_grant
        )
        return True
    
    def assign_role(
        self,
        user_id: UUID,
        role_name: str,
        assigner_id: UUID
    ) -> bool:
        """Assign a role to a user."""
        if role_name not in self._roles:
            return False
            
        role = self._roles[role_name]
        assigner_roles = self._user_roles.get(assigner_id, set())
        
        # Check if assigner has permission to grant all permissions in the role
        can_grant = False
        for assigner_role_name in assigner_roles:
            assigner_role = self._roles[assigner_role_name]
            if role.permissions.issubset(assigner_role.can_grant):
                can_grant = True
                break
                
        if not can_grant:
            return False
            
        if user_id not in self._user_roles:
            self._user_roles[user_id] = set()
        self._user_roles[user_id].add(role_name)
        return True
        
    def remove_role(
        self,
        user_id: UUID,
        role_name: str,
        remover_id: UUID
    ) -> bool:
        """Remove a role from a user."""
        if user_id not in self._user_roles or role_name not in self._roles:
            return False
            
        role = self._roles[role_name]
        remover_roles = self._user_roles.get(remover_id, set())
        
        # Check if remover has permission to remove all permissions in the role
        can_remove = False
        for remover_role_name in remover_roles:
            remover_role = self._roles[remover_role_name]
            if role.permissions.issubset(remover_role.can_grant):
                can_remove = True
                break
                
        if not can_remove:
            return False
            
        self._user_roles[user_id].discard(role_name)
        return True
    
    def has_permission(self, user_id: UUID, permission: Permission) -> bool:
        """Check if a user has a specific permission."""
        user_roles = self._user_roles.get(user_id, set())
        
        for role_name in user_roles:
            role = self._roles[role_name]
            if permission in role.permissions:
                return True
                
        return False
        
    def get_user_permissions(self, user_id: UUID) -> Set[Permission]:
        """Get all permissions a user has."""
        user_roles = self._user_roles.get(user_id, set())
        permissions = set()
        
        for role_name in user_roles:
            role = self._roles[role_name]
            permissions.update(role.permissions)
            
        return permissions 