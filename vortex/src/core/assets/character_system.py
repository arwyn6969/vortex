"""Enhanced character system with advanced features for NPCs and interactive characters."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Any
from datetime import datetime, time

class CharacterRole(Enum):
    """Possible roles for characters."""
    MERCHANT = "merchant"
    QUEST_GIVER = "quest_giver"
    MENTOR = "mentor"
    COMPANION = "companion"
    ANTAGONIST = "antagonist"
    NEUTRAL = "neutral"
    GUARDIAN = "guardian"
    SAGE = "sage"
    TRICKSTER = "trickster"
    CRAFTSMAN = "craftsman"

class DialogueStyle(Enum):
    """Character dialogue styles."""
    FORMAL = "formal"
    CASUAL = "casual"
    MYSTERIOUS = "mysterious"
    SCHOLARLY = "scholarly"
    POETIC = "poetic"
    HUMOROUS = "humorous"
    CRYPTIC = "cryptic"
    WISE = "wise"
    AGGRESSIVE = "aggressive"
    FRIENDLY = "friendly"

class EmotionalState(Enum):
    """Possible emotional states for characters."""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    NEUTRAL = "neutral"
    EXCITED = "excited"
    CURIOUS = "curious"
    SUSPICIOUS = "suspicious"
    FRIENDLY = "friendly"
    HOSTILE = "hostile"

class RelationType(Enum):
    """Types of relationships between characters."""
    FRIEND = "friend"
    ENEMY = "enemy"
    MENTOR = "mentor"
    STUDENT = "student"
    RIVAL = "rival"
    FAMILY = "family"
    BUSINESS = "business"
    ROMANTIC = "romantic"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"

class PondCondition(Enum):
    """Environmental conditions of a pond."""
    PRISTINE = "pristine"
    MURKY = "murky"
    POLLUTED = "polluted"
    STAGNANT = "stagnant"
    FLOWING = "flowing"
    SEASONAL = "seasonal"
    DROUGHT = "drought"
    FLOODED = "flooded"

class PondCharacterType(Enum):
    """Types of pond-specific characters."""
    FISH = "fish"
    AMPHIBIAN = "amphibian"
    CRUSTACEAN = "crustacean"
    INSECT = "insect"
    PLANT = "plant"
    SPIRIT = "spirit"
    GUARDIAN = "guardian"

@dataclass
class Relationship:
    """Represents a relationship between characters."""
    relation_type: RelationType
    strength: float  # 0.0 to 1.0
    trust: float  # 0.0 to 1.0
    history: List[Dict[str, Any]]  # List of interaction records
    last_interaction: Optional[datetime] = None
    custom_notes: Optional[str] = None

@dataclass
class Schedule:
    """Character's daily schedule."""
    daily_routines: Dict[str, List[Dict[str, Any]]]  # Day -> list of activities
    special_events: List[Dict[str, Any]]
    preferred_locations: Dict[str, float]  # Location -> preference weight
    availability_hours: Dict[str, tuple[time, time]]  # Day -> (start, end)
    
    @classmethod
    def create_default(cls) -> 'Schedule':
        """Create a default schedule."""
        return cls(
            daily_routines={
                "default": [
                    {
                        "time": "morning",
                        "activity": "idle",
                        "location": "home",
                        "duration": 60
                    }
                ]
            },
            special_events=[],
            preferred_locations={"home": 1.0},
            availability_hours={"default": (time(9, 0), time(17, 0))}
        )

@dataclass
class Stats:
    """Character statistics and attributes."""
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    vitality: int = 10
    magic: int = 10
    luck: int = 10
    
    # Derived stats
    max_health: int = 100
    max_mana: int = 100
    physical_defense: int = 10
    magical_defense: int = 10
    
    # Dynamic stats
    current_health: int = 100
    current_mana: int = 100
    fatigue: int = 0
    morale: int = 100

@dataclass
class Ability:
    """Character ability or skill."""
    name: str
    description: str
    type: str
    level: int
    experience: int
    max_level: int
    requirements: Dict[str, Any]
    effects: List[Dict[str, Any]]
    cooldown: float
    resource_cost: Dict[str, int]
    unlocked: bool = False

@dataclass
class Knowledge:
    """Character's knowledge and information."""
    topics: Set[str]
    skills: Dict[str, int]  # skill -> proficiency level
    languages: Dict[str, float]  # language -> proficiency (0.0 to 1.0)
    lore: Set[str]  # Known lore/story elements
    secrets: Set[str]  # Known secrets
    quest_knowledge: Dict[str, Any]  # Quest-related knowledge
    memories: List[Dict[str, Any]]  # Important memories/events

@dataclass
class PondAttributes:
    """Attributes specific to pond-dwelling characters."""
    home_pond: str  # ID of the character's home pond
    pond_type: PondCharacterType
    sefirot_attunement: SefirotAttribute  # Character's attunement to pond's Sefirot energy
    elemental_affinity: str  # Alignment with pond's element
    symbolic_resonance: Dict[str, float]  # Resonance with pond's symbols (0.0 to 1.0)
    depth_preference: tuple[float, float]  # Preferred min and max depth in meters
    temperature_range: tuple[float, float]  # Preferred min and max temperature
    migration_enabled: bool = False  # Whether character can move between ponds
    migration_triggers: List[Dict[str, Any]] = None  # Conditions that trigger migration
    territorial_range: float = 1.0  # Range in meters the character patrols/inhabits
    seasonal_behaviors: Dict[str, Dict[str, Any]] = None  # Season-specific behavior changes
    dimensional_requirements: Dict[ProfileDimension, float] = None  # Required profile dimensions for interaction
    pond_specific_actions: Set[str] = None  # Actions only available in this pond
    environmental_responses: Dict[str, Dict[str, Any]] = None  # How character responds to pond conditions

@dataclass
class Behavior:
    """Character behavior patterns and AI."""
    personality_traits: Dict[str, float]
    decision_weights: Dict[str, float]
    interaction_preferences: Dict[str, float]
    emotional_state: EmotionalState
    mood_modifiers: List[Dict[str, Any]]
    conversation_topics: List[str]
    response_patterns: Dict[str, List[str]]
    ai_directives: Dict[str, Any]
    pond_attributes: Optional[PondAttributes] = None  # Pond-specific attributes if character is pond-bound

class CharacterSystem:
    """Advanced character management system."""
    
    @staticmethod
    def validate_stats(stats: Dict[str, Any]) -> Stats:
        """Validate and create Stats object."""
        valid_stats = Stats()
        for key, value in stats.items():
            if hasattr(valid_stats, key):
                if not isinstance(value, int):
                    raise ValueError(f"Stat {key} must be an integer")
                if value < 0:
                    raise ValueError(f"Stat {key} cannot be negative")
                setattr(valid_stats, key, value)
        return valid_stats
    
    @staticmethod
    def validate_ability(ability: Dict[str, Any]) -> Ability:
        """Validate and create Ability object."""
        required = {
            "name", "description", "type", "level", "experience",
            "max_level", "requirements", "effects", "cooldown", "resource_cost"
        }
        missing = required - set(ability.keys())
        if missing:
            raise ValueError(f"Missing required ability fields: {missing}")
            
        return Ability(**ability)
    
    @staticmethod
    def validate_schedule(schedule: Dict[str, Any]) -> Schedule:
        """Validate and create Schedule object."""
        if not schedule:
            return Schedule.create_default()
            
        # Validate time formats and activities
        for day, routines in schedule.get("daily_routines", {}).items():
            for routine in routines:
                if not all(k in routine for k in ["time", "activity", "location", "duration"]):
                    raise ValueError(f"Invalid routine format in schedule for day {day}")
                
        return Schedule(
            daily_routines=schedule.get("daily_routines", {}),
            special_events=schedule.get("special_events", []),
            preferred_locations=schedule.get("preferred_locations", {}),
            availability_hours=schedule.get("availability_hours", {})
        )
    
    @staticmethod
    def validate_knowledge(knowledge: Dict[str, Any]) -> Knowledge:
        """Validate and create Knowledge object."""
        return Knowledge(
            topics=set(knowledge.get("topics", [])),
            skills=knowledge.get("skills", {}),
            languages=knowledge.get("languages", {}),
            lore=set(knowledge.get("lore", [])),
            secrets=set(knowledge.get("secrets", [])),
            quest_knowledge=knowledge.get("quest_knowledge", {}),
            memories=knowledge.get("memories", [])
        )
    
    @staticmethod
    def validate_pond_attributes(pond_data: Dict[str, Any]) -> Optional[PondAttributes]:
        """Validate and create PondAttributes object."""
        if not pond_data:
            return None
            
        required = {
            "home_pond", 
            "pond_type", 
            "sefirot_attunement",
            "elemental_affinity",
            "symbolic_resonance",
            "depth_preference", 
            "temperature_range"
        }
        missing = required - set(pond_data.keys())
        if missing:
            raise ValueError(f"Missing required pond attribute fields: {missing}")
        
        try:
            pond_type = PondCharacterType(pond_data["pond_type"])
            sefirot = SefirotAttribute(pond_data["sefirot_attunement"])
            symbolic_resonance = {
                k: max(0.0, min(1.0, float(v)))
                for k, v in pond_data.get("symbolic_resonance", {}).items()
            }
        except ValueError as e:
            raise ValueError(f"Invalid pond type, sefirot, or resonance: {e}")
            
        depth_pref = pond_data["depth_preference"]
        temp_range = pond_data["temperature_range"]
        if not (isinstance(depth_pref, (list, tuple)) and len(depth_pref) == 2):
            raise ValueError("depth_preference must be a tuple of (min, max)")
        if not (isinstance(temp_range, (list, tuple)) and len(temp_range) == 2):
            raise ValueError("temperature_range must be a tuple of (min, max)")
            
        dimensional_requirements = {}
        for dim_name, value in pond_data.get("dimensional_requirements", {}).items():
            try:
                dim = ProfileDimension(dim_name)
                dimensional_requirements[dim] = max(0.0, min(1.0, float(value)))
            except ValueError:
                continue
                
        return PondAttributes(
            home_pond=pond_data["home_pond"],
            pond_type=pond_type,
            sefirot_attunement=sefirot,
            elemental_affinity=pond_data["elemental_affinity"],
            symbolic_resonance=symbolic_resonance,
            depth_preference=(float(depth_pref[0]), float(depth_pref[1])),
            temperature_range=(float(temp_range[0]), float(temp_range[1])),
            migration_enabled=pond_data.get("migration_enabled", False),
            migration_triggers=pond_data.get("migration_triggers"),
            territorial_range=float(pond_data.get("territorial_range", 1.0)),
            seasonal_behaviors=pond_data.get("seasonal_behaviors"),
            dimensional_requirements=dimensional_requirements,
            pond_specific_actions=set(pond_data.get("pond_specific_actions", [])),
            environmental_responses=pond_data.get("environmental_responses", {})
        )

    @staticmethod
    def validate_behavior(behavior: Dict[str, Any]) -> Behavior:
        """Validate and create Behavior object."""
        try:
            emotional_state = EmotionalState(behavior.get("emotional_state", "neutral"))
        except ValueError:
            emotional_state = EmotionalState.NEUTRAL
            
        pond_attributes = None
        if "pond_attributes" in behavior:
            pond_attributes = CharacterSystem.validate_pond_attributes(behavior["pond_attributes"])
            
        return Behavior(
            personality_traits=behavior.get("personality_traits", {}),
            decision_weights=behavior.get("decision_weights", {}),
            interaction_preferences=behavior.get("interaction_preferences", {}),
            emotional_state=emotional_state,
            mood_modifiers=behavior.get("mood_modifiers", []),
            conversation_topics=behavior.get("conversation_topics", []),
            response_patterns=behavior.get("response_patterns", {}),
            ai_directives=behavior.get("ai_directives", {}),
            pond_attributes=pond_attributes
        )
    
    @staticmethod
    def validate_relationships(relationships: Dict[str, Any]) -> Dict[str, Relationship]:
        """Validate and create relationship mappings."""
        validated = {}
        for char_id, rel_data in relationships.items():
            try:
                rel_type = RelationType(rel_data.get("type", "neutral"))
            except ValueError:
                rel_type = RelationType.NEUTRAL
                
            validated[char_id] = Relationship(
                relation_type=rel_type,
                strength=min(1.0, max(0.0, rel_data.get("strength", 0.0))),
                trust=min(1.0, max(0.0, rel_data.get("trust", 0.0))),
                history=rel_data.get("history", []),
                last_interaction=rel_data.get("last_interaction"),
                custom_notes=rel_data.get("custom_notes")
            )
        return validated
    
    @classmethod
    def create_character_template(cls) -> Dict[str, Any]:
        """Create a complete character template with all features."""
        return {
            "required_fields": {
                "name",
                "description",
                "role",
                "dialogue_style"
            },
            "optional_fields": {
                "stats",
                "abilities",
                "schedule",
                "relationships",
                "knowledge",
                "behavior",
                "appearance",
                "inventory",
                "faction",
                "level",
                "experience",
                "tags",
                "custom_data"
            },
            "validators": {
                "stats": cls.validate_stats,
                "abilities": lambda x: [cls.validate_ability(a) for a in x],
                "schedule": cls.validate_schedule,
                "relationships": cls.validate_relationships,
                "knowledge": cls.validate_knowledge,
                "behavior": cls.validate_behavior
            },
            "enums": {
                "role": CharacterRole,
                "dialogue_style": DialogueStyle,
                "emotional_state": EmotionalState,
                "relation_type": RelationType
            }
        } 