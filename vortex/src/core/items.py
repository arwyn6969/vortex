"""Item system for managing game items and their interactions."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Set

class ItemType(Enum):
    """Types of items that can exist in the game."""
    TOOL = auto()
    CONSUMABLE = auto()
    QUEST = auto()
    COSMETIC = auto()

@dataclass
class ItemProperties:
    """Properties that define an item's behavior and characteristics."""
    description: str
    can_be_picked_up: bool = True
    can_be_dropped: bool = True
    can_be_used: bool = False
    can_be_examined: bool = True
    use_message: Optional[str] = None
    examine_message: Optional[str] = None

class ItemRegistry:
    """Registry of all available items in the game."""
    
    def __init__(self):
        self._items: Dict[str, ItemProperties] = {}
        self._initialize_basic_items()
    
    def _initialize_basic_items(self):
        """Initialize the basic set of items available in the game."""
        self.register_item(
            "apple",
            ItemProperties(
                description="A shiny red apple that looks delicious.",
                can_be_used=True,
                use_message="You eat the apple. It's crisp and refreshing.",
                examine_message="The apple is perfectly ripe and gives off a sweet aroma."
            )
        )
        
        self.register_item(
            "towel",
            ItemProperties(
                description="A large, fluffy towel. Essential for any galactic hitchhiker.",
                examine_message="The towel is large, soft, and incredibly useful. As the Hitchhiker's Guide says, a towel is about the most massively useful thing an interstellar hitchhiker can have."
            )
        )
        
        self.register_item(
            "dressing_gown",
            ItemProperties(
                description="A comfortable dressing gown, perfect for lounging.",
                examine_message="The dressing gown is made of soft material and has deep pockets."
            )
        )
        
        self.register_item(
            "rubber_chicken_with_pulley",
            ItemProperties(
                description="A rubber chicken with a pulley in the middle. Seems useful... somehow.",
                examine_message="It's exactly what it says on the tin: a rubber chicken with a pulley in the middle. The engineering is quite impressive."
            )
        )
        
        self.register_item(
            "wax_lips",
            ItemProperties(
                description="A pair of novelty wax lips.",
                can_be_used=True,
                use_message="You put on the wax lips. You look ridiculous, but feel amazing.",
                examine_message="These wax lips are bright red and slightly waxy (obviously)."
            )
        )
    
    def register_item(self, item_id: str, properties: ItemProperties) -> None:
        """Register a new item type in the system."""
        if not item_id or not isinstance(item_id, str):
            raise ValueError("Invalid item ID")
        if item_id in self._items:
            raise ValueError(f"Item {item_id} already registered")
        
        self._items[item_id] = properties
    
    def get_item_properties(self, item_id: str) -> Optional[ItemProperties]:
        """Get the properties of an item by its ID."""
        return self._items.get(item_id)
    
    def item_exists(self, item_id: str) -> bool:
        """Check if an item exists in the registry."""
        return item_id in self._items
    
    def get_all_items(self) -> List[str]:
        """Get a list of all registered item IDs."""
        return list(self._items.keys()) 