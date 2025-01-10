"""Templates and validation rules for different asset types."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Any, Callable
from enum import Enum

from .character_system import (
    CharacterSystem,
    CharacterRole,
    DialogueStyle,
    EmotionalState,
    RelationType
)

class ValidationError(Exception):
    """Raised when asset validation fails."""
    pass

@dataclass
class AssetTemplate:
    """Template for an asset type with validation rules."""
    required_fields: Set[str]
    optional_fields: Set[str]
    field_types: Dict[str, type]
    field_validators: Dict[str, Callable[[Any], bool]]
    field_defaults: Dict[str, Any]
    description: str

class ItemCategory(Enum):
    """Categories for items."""
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    QUEST = "quest"
    TOOL = "tool"
    COSMETIC = "cosmetic"
    MAGICAL = "magical"

class AssetTemplates:
    """Manages templates for different asset types."""
    
    def __init__(self):
        self._character_system = CharacterSystem()
    
    @staticmethod
    def validate_damage(value: Dict) -> bool:
        """Validate damage object."""
        required = {"min", "max", "type"}
        return (
            isinstance(value, dict) 
            and all(k in value for k in required)
            and isinstance(value["min"], (int, float))
            and isinstance(value["max"], (int, float))
            and value["min"] <= value["max"]
        )
    
    @staticmethod
    def validate_effects(value: List) -> bool:
        """Validate effects list."""
        return (
            isinstance(value, list)
            and all(isinstance(e, dict) and "type" in e for e in value)
        )
    
    @staticmethod
    def validate_requirements(value: Dict) -> bool:
        """Validate requirements object."""
        return (
            isinstance(value, dict)
            and all(isinstance(v, (int, float)) for v in value.values())
        )
    
    @classmethod
    def get_item_template(cls) -> AssetTemplate:
        """Get template for items."""
        return AssetTemplate(
            required_fields={
                "name",
                "description",
                "category"
            },
            optional_fields={
                "damage",
                "defense",
                "effects",
                "durability",
                "requirements",
                "cooldown",
                "stackable",
                "unique",
                "tradeable",
                "value",
                "weight",
                "level",
                "rarity"
            },
            field_types={
                "name": str,
                "description": str,
                "category": ItemCategory,
                "damage": dict,
                "defense": int,
                "effects": list,
                "durability": int,
                "requirements": dict,
                "cooldown": float,
                "stackable": bool,
                "unique": bool,
                "tradeable": bool,
                "value": int,
                "weight": float,
                "level": int,
                "rarity": str
            },
            field_validators={
                "damage": cls.validate_damage,
                "effects": cls.validate_effects,
                "requirements": cls.validate_requirements
            },
            field_defaults={
                "stackable": False,
                "unique": False,
                "tradeable": True,
                "value": 0,
                "weight": 1.0,
                "level": 1,
                "rarity": "common"
            },
            description="Template for creating game items"
        )
    
    @classmethod
    def get_character_template(cls) -> AssetTemplate:
        """Get template for characters."""
        char_template = cls._character_system.create_character_template()
        
        return AssetTemplate(
            required_fields=char_template["required_fields"],
            optional_fields=char_template["optional_fields"],
            field_types={
                "name": str,
                "description": str,
                "role": CharacterRole,
                "dialogue_style": DialogueStyle,
                "stats": dict,
                "abilities": list,
                "schedule": dict,
                "relationships": dict,
                "knowledge": dict,
                "behavior": dict,
                "appearance": dict,
                "inventory": list,
                "faction": str,
                "level": int,
                "experience": int,
                "tags": list,
                "custom_data": dict
            },
            field_validators=char_template["validators"],
            field_defaults={
                "level": 1,
                "experience": 0,
                "inventory": [],
                "tags": [],
                "custom_data": {}
            },
            description="Template for creating game characters"
        )
    
    @classmethod
    def get_scene_template(cls) -> AssetTemplate:
        """Get template for scenes."""
        return AssetTemplate(
            required_fields={
                "name",
                "description",
                "type",
                "entry_points"
            },
            optional_fields={
                "exits",
                "items",
                "npcs",
                "triggers",
                "environment",
                "weather",
                "time",
                "music",
                "ambiance",
                "interactions"
            },
            field_types={
                "name": str,
                "description": str,
                "type": str,
                "entry_points": list,
                "exits": dict,
                "items": list,
                "npcs": list,
                "triggers": list,
                "environment": dict,
                "weather": str,
                "time": str,
                "music": str,
                "ambiance": list,
                "interactions": list
            },
            field_validators={},  # Add specific validators as needed
            field_defaults={
                "exits": {},
                "items": [],
                "npcs": [],
                "triggers": [],
                "environment": {},
                "weather": "clear",
                "time": "day",
                "ambiance": []
            },
            description="Template for creating game scenes"
        )
    
    @classmethod
    def validate_asset(cls, asset_type: str, content: Dict[str, Any]) -> None:
        """Validate asset content against its template."""
        template = getattr(cls, f"get_{asset_type.lower()}_template")()
        
        # Check required fields
        missing_fields = template.required_fields - set(content.keys())
        if missing_fields:
            raise ValidationError(
                f"Missing required fields for {asset_type}: {missing_fields}"
            )
        
        # Check field types and run validators
        for field, value in content.items():
            if field not in template.required_fields | template.optional_fields:
                raise ValidationError(f"Unknown field for {asset_type}: {field}")
            
            expected_type = template.field_types.get(field)
            if expected_type and not isinstance(value, expected_type):
                if expected_type in [CharacterRole, DialogueStyle, ItemCategory] and isinstance(value, str):
                    try:
                        expected_type(value.lower())
                    except ValueError:
                        raise ValidationError(
                            f"Invalid {field}: {value}. Must be one of {[e.value for e in expected_type]}"
                        )
                else:
                    raise ValidationError(
                        f"Field {field} must be of type {expected_type.__name__}"
                    )
            
            validator = template.field_validators.get(field)
            if validator and not validator(value):
                raise ValidationError(f"Validation failed for field: {field}")
    
    @classmethod
    def apply_defaults(cls, asset_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Apply template defaults to asset content."""
        template = getattr(cls, f"get_{asset_type.lower()}_template")()
        result = content.copy()
        
        for field, default in template.field_defaults.items():
            if field not in result:
                result[field] = default
        
        return result 