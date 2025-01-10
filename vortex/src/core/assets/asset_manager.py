"""Asset management system for handling game assets."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union, Set, Tuple
from uuid import UUID, uuid4

from ..permissions import PermissionManager, Permission
from .templates import AssetTemplates, ValidationError

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
    collaborators: Set[UUID] = None
    forks_from: Optional[UUID] = None
    fork_version: Optional[int] = None
    ratings: Dict[UUID, float] = None
    comments: List[Dict[str, Any]] = None

    def __post_init__(self):
        self.collaborators = self.collaborators or set()
        self.ratings = self.ratings or {}
        self.comments = self.comments or []

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
        self._templates = AssetTemplates()
        self._forks: Dict[UUID, Set[UUID]] = {}  # original -> set of forks
    
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
        
        # Validate content against template
        try:
            self._templates.validate_asset(asset_type.name, content)
            content = self._templates.apply_defaults(asset_type.name, content)
        except ValidationError as e:
            raise ValueError(f"Content validation failed: {str(e)}")
        
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
            approved=not require_approval,  # Auto-approve if not required
            collaborators={creator_id}  # Creator is automatically a collaborator
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
            "timestamp": now,
            "editor_id": creator_id
        }]
        
        return asset_id
    
    def fork_asset(
        self,
        asset_id: UUID,
        forker_id: UUID,
        new_properties: Optional[Dict[str, Any]] = None
    ) -> Optional[UUID]:
        """Create a fork of an existing asset."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return None
            
        original = self._assets[asset_id]
        content = self._asset_contents[asset_id]
        
        # Check permissions
        required_permission = getattr(Permission, f"CREATE_{original.asset_type.name}")
        if not self._permission_manager.has_permission(forker_id, required_permission):
            return None
        
        # Create fork with original content
        fork_id = self.create_asset(
            asset_type=original.asset_type,
            content=content.data,
            content_type=content.content_type,
            creator_id=forker_id,
            properties={**original.properties, **(new_properties or {})},
            tags=original.tags.copy()
        )
        
        if fork_id:
            # Update fork metadata
            fork = self._assets[fork_id]
            fork.forks_from = asset_id
            fork.fork_version = original.version
            
            # Track fork relationship
            if asset_id not in self._forks:
                self._forks[asset_id] = set()
            self._forks[asset_id].add(fork_id)
        
        return fork_id
    
    def add_collaborator(
        self,
        asset_id: UUID,
        collaborator_id: UUID,
        adder_id: UUID
    ) -> bool:
        """Add a collaborator to an asset."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return False
            
        metadata = self._assets[asset_id]
        
        # Check if adder has permission
        if (
            adder_id != metadata.creator_id
            and adder_id not in metadata.collaborators
            and not self._permission_manager.has_permission(adder_id, Permission.ADMIN)
        ):
            return False
        
        metadata.collaborators.add(collaborator_id)
        return True
    
    def remove_collaborator(
        self,
        asset_id: UUID,
        collaborator_id: UUID,
        remover_id: UUID
    ) -> bool:
        """Remove a collaborator from an asset."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return False
            
        metadata = self._assets[asset_id]
        
        # Check if remover has permission
        if (
            remover_id != metadata.creator_id
            and remover_id not in metadata.collaborators
            and not self._permission_manager.has_permission(remover_id, Permission.ADMIN)
        ):
            return False
        
        # Can't remove the creator
        if collaborator_id == metadata.creator_id:
            return False
        
        metadata.collaborators.discard(collaborator_id)
        return True
    
    def rate_asset(
        self,
        asset_id: UUID,
        rater_id: UUID,
        rating: float
    ) -> bool:
        """Rate an asset (1-5 scale)."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return False
            
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
            
        metadata = self._assets[asset_id]
        metadata.ratings[rater_id] = rating
        return True
    
    def add_comment(
        self,
        asset_id: UUID,
        commenter_id: UUID,
        content: str,
        parent_id: Optional[UUID] = None
    ) -> Optional[UUID]:
        """Add a comment to an asset."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return None
            
        metadata = self._assets[asset_id]
        comment_id = uuid4()
        
        comment = {
            "id": comment_id,
            "content": content,
            "commenter_id": commenter_id,
            "timestamp": datetime.utcnow(),
            "parent_id": parent_id,
            "edited": False
        }
        
        metadata.comments.append(comment)
        return comment_id
    
    def edit_comment(
        self,
        asset_id: UUID,
        comment_id: UUID,
        editor_id: UUID,
        new_content: str
    ) -> bool:
        """Edit a comment."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return False
            
        metadata = self._assets[asset_id]
        
        for comment in metadata.comments:
            if comment["id"] == comment_id:
                if comment["commenter_id"] != editor_id:
                    return False
                    
                comment["content"] = new_content
                comment["edited"] = True
                return True
                
        return False
    
    def get_asset_rating(self, asset_id: UUID) -> Optional[float]:
        """Get average rating for an asset."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return None
            
        metadata = self._assets[asset_id]
        if not metadata.ratings:
            return None
            
        return sum(metadata.ratings.values()) / len(metadata.ratings)
    
    def get_asset_comments(
        self,
        asset_id: UUID,
        parent_id: Optional[UUID] = None
    ) -> List[Dict[str, Any]]:
        """Get comments for an asset, optionally filtered by parent_id."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return []
            
        metadata = self._assets[asset_id]
        return [
            c for c in metadata.comments
            if c["parent_id"] == parent_id
        ]
    
    def get_asset_forks(self, asset_id: UUID) -> Set[UUID]:
        """Get all forks of an asset."""
        return self._forks.get(asset_id, set())
    
    def get_fork_tree(self, asset_id: UUID) -> Dict[str, Any]:
        """Get the complete fork tree of an asset."""
        if asset_id not in self._assets:
            return {}
            
        def build_tree(current_id: UUID) -> Dict[str, Any]:
            metadata = self._assets[current_id]
            tree = {
                "id": current_id,
                "creator": metadata.creator_id,
                "version": metadata.version,
                "forks": []
            }
            
            for fork_id in self._forks.get(current_id, set()):
                if not self._assets[fork_id].is_deleted:
                    tree["forks"].append(build_tree(fork_id))
                    
            return tree
            
        return build_tree(asset_id)
    
    def merge_fork(
        self,
        fork_id: UUID,
        merger_id: UUID
    ) -> bool:
        """Merge a fork back into its original asset."""
        if fork_id not in self._assets or self._assets[fork_id].is_deleted:
            return False
            
        fork = self._assets[fork_id]
        if not fork.forks_from:
            return False
            
        original_id = fork.forks_from
        if original_id not in self._assets or self._assets[original_id].is_deleted:
            return False
            
        original = self._assets[original_id]
        
        # Check permissions
        if (
            merger_id not in original.collaborators
            and not self._permission_manager.has_permission(merger_id, Permission.ADMIN)
        ):
            return False
        
        # Create new version of original with fork's content
        return self.update_asset(
            asset_id=original_id,
            editor_id=merger_id,
            content=self._asset_contents[fork_id].data
        )
    
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