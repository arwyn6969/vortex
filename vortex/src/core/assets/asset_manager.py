"""Asset management system for handling game assets."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union, Set
from uuid import UUID, uuid4

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

class AssetManager:
    """Manages all game assets including scenes, characters, and items."""
    
    def __init__(self):
        self._assets: Dict[UUID, AssetMetadata] = {}
        self._asset_contents: Dict[UUID, AssetContent] = {}
        self._type_index: Dict[AssetType, Set[UUID]] = {
            asset_type: set() for asset_type in AssetType
        }
    
    def create_asset(
        self,
        asset_type: Union[str, AssetType],
        content: Any,
        content_type: str,
        creator_id: Optional[UUID] = None,
        properties: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> UUID:
        """Create a new asset and return its ID."""
        # Validate asset type
        if isinstance(asset_type, str):
            try:
                asset_type = AssetType[asset_type.upper()]
            except KeyError:
                raise ValueError(f"Invalid asset type: {asset_type}")
        
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
            is_deleted=False
        )
        
        # Create content
        content_obj = AssetContent(
            data=content,
            content_type=content_type,
            size=len(str(content)),  # Basic size calculation
            checksum=str(hash(str(content)))  # Basic checksum
        )
        
        self._assets[asset_id] = metadata
        self._asset_contents[asset_id] = content_obj
        self._type_index[asset_type].add(asset_id)
        
        return asset_id
    
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
    
    def update_asset(
        self,
        asset_id: UUID,
        content: Optional[Any] = None,
        properties: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Update an existing asset's metadata and/or content."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return False
            
        metadata = self._assets[asset_id]
        if properties is not None:
            metadata.properties.update(properties)
        if tags is not None:
            metadata.tags = tags
        metadata.last_modified = datetime.utcnow()
        
        if content is not None:
            content_obj = self._asset_contents[asset_id]
            content_obj.data = content
            content_obj.size = len(str(content))
            content_obj.checksum = str(hash(str(content)))
        
        return True
    
    def delete_asset(self, asset_id: UUID) -> bool:
        """Mark an asset as deleted."""
        if asset_id not in self._assets or self._assets[asset_id].is_deleted:
            return False
            
        metadata = self._assets[asset_id]
        metadata.is_deleted = True
        metadata.last_modified = datetime.utcnow()
        
        # Remove from type index
        self._type_index[metadata.asset_type].remove(asset_id)
        
        return True
    
    def query_assets(
        self,
        asset_type: Optional[Union[str, AssetType]] = None,
        tags: Optional[List[str]] = None,
        creator_id: Optional[UUID] = None
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
            if not metadata.is_deleted
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