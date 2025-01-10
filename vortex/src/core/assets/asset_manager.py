"""Asset management system for handling game assets."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union, Set
from uuid import UUID, uuid4

from ..permissions import PermissionManager, Permission

class AssetType(Enum):
    """Valid types of assets in the system."""
    SCENE = auto()
    CHARACTER = auto()
    ITEM = auto()
    LOOT = auto()
    STAMP = auto()
    NFT = auto()

@dataclass
class AssetContent:
    """Content of an asset."""
    data: Any
    content_type: str
    size: int
    checksum: str

@dataclass
class AssetMetadata:
    """Metadata for any game asset."""
    asset_id: UUID
    asset_type: AssetType
    creator_id: Optional[UUID]
    creation_date: datetime
    last_modified: datetime
    tags: List[str]
    properties: Dict[str, Any]
    is_deleted: bool = False
    version: int = 1
    approved: bool = False
    approved_by: Optional[UUID] = None
    approval_date: Optional[datetime] = None

class AssetManager:
    """Manages all game assets including scenes, characters, and items."""
    
    def __init__(self, permission_manager: PermissionManager):
        self._assets: Dict[UUID, AssetMetadata] = {}
        self._asset_contents: Dict[UUID, AssetContent] = {}
        self._type_index: Dict[AssetType, Set[UUID]] = {
            asset_type: set() for asset_type in AssetType
        }
        self._permission_manager = permission_manager
        self._version_history: Dict[UUID, List[Dict[str, Any]]] = {}
    
    def create_asset(
        self,
        asset_type: Union[str, AssetType],
        content: Any,
        content_type: str,
        creator_id: UUID,
        properties: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        require_approval: bool = True
    ) -> Optional[UUID]:
        """Create a new asset and return its ID."""
        # Validate asset type and permissions
        if isinstance(asset_type, str):
            try:
                asset_type = AssetType[asset_type.upper()]
            except KeyError:
                raise ValueError(f"Invalid asset type: {asset_type}")
        
        # Check permissions
        required_permission = getattr(Permission, f"CREATE_{asset_type.name}")
        if not self._permission_manager.has_permission(creator_id, required_permission):
            return None
        
        asset_id = uuid4()
        now = datetime.utcnow()
        
        # Create metadata
        metadata = AssetMetadata(
            asset_id=asset_id,
            asset_type=asset_type,
            creator_id=creator_id,
            creation_date=now,
            last_modified=now,
            tags=tags or [],
            properties=properties or {},
            is_deleted=False,
            version=1,
            approved=not require_approval  # Auto-approve if not required
        )
        
        # Create content
        content_obj = AssetContent(
            data=content,
            content_type=content_type,
            size=len(str(content)),
            checksum=str(hash(str(content)))
        )
        
        self._assets[asset_id] = metadata
        self._asset_contents[asset_id] = content_obj
        self._type_index[asset_type].add(asset_id)
        
        # Initialize version history
        self._version_history[asset_id] = [{
            "version": 1,
            "content": content,
            "metadata": metadata,
            "timestamp": now
        }]
        
        return asset_id
    
    def update_asset(
        self,
        asset_id: UUID,
        editor_id: UUID,
        content: Optional[Any] = None,
        properties: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        require_approval: bool = True
    ) -> bool:
        """Update an existing asset's metadata and/or content."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return False
            
        metadata = self._assets[asset_id]
        
        # Check permissions
        required_permission = getattr(Permission, f"MODIFY_{metadata.asset_type.name}")
        if not self._permission_manager.has_permission(editor_id, required_permission):
            return False
            
        # Create new version
        now = datetime.utcnow()
        metadata.version += 1
        metadata.last_modified = now
        metadata.approved = not require_approval
        metadata.approved_by = None
        metadata.approval_date = None
        
        if properties is not None:
            metadata.properties.update(properties)
        if tags is not None:
            metadata.tags = tags
        
        if content is not None:
            content_obj = self._asset_contents[asset_id]
            content_obj.data = content
            content_obj.size = len(str(content))
            content_obj.checksum = str(hash(str(content)))
            
            # Add to version history
            self._version_history[asset_id].append({
                "version": metadata.version,
                "content": content,
                "metadata": metadata,
                "timestamp": now
            })
        
        return True
    
    def approve_asset(
        self,
        asset_id: UUID,
        approver_id: UUID
    ) -> bool:
        """Approve an asset version."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return False
            
        metadata = self._assets[asset_id]
        
        # Check if approver has moderator permissions
        if not self._permission_manager.has_permission(approver_id, Permission.ADMIN):
            return False
            
        metadata.approved = True
        metadata.approved_by = approver_id
        metadata.approval_date = datetime.utcnow()
        
        return True
    
    def get_version_history(
        self,
        asset_id: UUID,
        viewer_id: UUID
    ) -> Optional[List[Dict[str, Any]]]:
        """Get the version history of an asset."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return None
            
        metadata = self._assets[asset_id]
        required_permission = getattr(Permission, f"MODIFY_{metadata.asset_type.name}")
        
        if not self._permission_manager.has_permission(viewer_id, required_permission):
            return None
            
        return self._version_history[asset_id]
    
    def get_asset_metadata(self, asset_id: UUID) -> Optional[AssetMetadata]:
        """Retrieve metadata for an asset."""
        metadata = self._assets.get(asset_id)
        if metadata and metadata.is_deleted:
            return None
        return metadata
    
    def get_asset_content(self, asset_id: UUID) -> Optional[AssetContent]:
        """Retrieve content for an asset."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return None
        return self._asset_contents.get(asset_id)
    
    def delete_asset(
        self,
        asset_id: UUID,
        deleter_id: UUID
    ) -> bool:
        """Mark an asset as deleted."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return False
            
        metadata = self._assets[asset_id]
        required_permission = getattr(Permission, f"DELETE_{metadata.asset_type.name}")
        
        if not self._permission_manager.has_permission(deleter_id, required_permission):
            return False
            
        metadata.is_deleted = True
        metadata.last_modified = datetime.utcnow()
        
        # Remove from type index
        self._type_index[metadata.asset_type].remove(asset_id)
        
        return True
    
    def query_assets(
        self,
        asset_type: Optional[Union[str, AssetType]] = None,
        tags: Optional[List[str]] = None,
        creator_id: Optional[UUID] = None,
        approved_only: bool = True
    ) -> List[AssetMetadata]:
        """Query assets based on type, tags, or creator."""
        # Convert string asset type to enum if needed
        if isinstance(asset_type, str):
            try:
                asset_type = AssetType[asset_type.upper()]
            except KeyError:
                raise ValueError(f"Invalid asset type: {asset_type}")
        
        # Start with all non-deleted assets
        candidates = {
            asset_id for asset_id, metadata in self._assets.items()
            if not metadata.is_deleted and (not approved_only or metadata.approved)
        }
        
        # Filter by type if specified
        if asset_type:
            candidates &= self._type_index[asset_type]
        
        # Apply remaining filters
        results = []
        for asset_id in candidates:
            metadata = self._assets[asset_id]
            if tags and not all(tag in metadata.tags for tag in tags):
                continue
            if creator_id and metadata.creator_id != creator_id:
                continue
            results.append(metadata)
        
        return sorted(results, key=lambda m: m.last_modified, reverse=True) 