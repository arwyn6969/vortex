"""
Manages cultural archetypes and their integration across different mythological systems.
"""
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum

class CulturalSystem(Enum):
    EGYPTIAN = "egyptian"
    MAYAN = "mayan"
    DOGON = "dogon"
    KABBALISTIC = "kabbalistic"
    JUNGIAN = "jungian"
    CAMPBELLIAN = "campbellian"
    TAROT = "tarot"
    NORSE = "norse"
    CELTIC = "celtic"
    HOPI = "hopi"

@dataclass
class ArchetypeMapping:
    """Maps equivalent archetypes across cultural systems."""
    name: str
    description: str
    cultural_variants: Dict[CulturalSystem, str]
    attributes: Set[str]
    resonant_dimensions: Set[str]
    celestial_correspondences: Optional[Set[str]] = None  # Associated celestial objects/events
    jungian_aspect: Optional[str] = None  # Core Jungian archetype
    hero_stage: Optional[str] = None      # Campbell's Hero's Journey stage
    tarot_cards: Optional[Set[str]] = None  # Associated Major Arcana

class ArchetypeManager:
    """Manages cross-cultural archetype mappings and integrations."""
    
    def __init__(self):
        self.archetype_mappings: Dict[str, ArchetypeMapping] = {}
        self._initialize_core_mappings()
    
    def _initialize_core_mappings(self) -> None:
        """Initialize core archetype mappings across cultures."""
        # Wisdom Teacher / Wise Old Man archetype
        self.archetype_mappings["wisdom_teacher"] = ArchetypeMapping(
            name="Wisdom Teacher",
            description="The sage who guides through knowledge and wisdom",
            cultural_variants={
                CulturalSystem.EGYPTIAN: "Thoth",
                CulturalSystem.MAYAN: "Itzamna",
                CulturalSystem.DOGON: "Nommo",
                CulturalSystem.KABBALISTIC: "Hochmah",
                CulturalSystem.JUNGIAN: "Wise Old Man",
                CulturalSystem.TAROT: "The Hierophant",
                CulturalSystem.NORSE: "Odin",
                CulturalSystem.CELTIC: "Taliesin",
                CulturalSystem.HOPI: "Masauwu"
            },
            attributes={"wisdom", "knowledge", "teaching", "guidance"},
            resonant_dimensions={"wisdom", "self_reflection", "consciousness_depth"},
            celestial_correspondences={"Winter Solstice", "Sirius"},
            jungian_aspect="Wise Old Man",
            hero_stage="Supernatural Aid",
            tarot_cards={"The Hierophant", "The Hermit"}
        )
        
        # Harmony Keeper / Anima archetype
        self.archetype_mappings["harmony_keeper"] = ArchetypeMapping(
            name="Harmony Keeper",
            description="The maintainer of balance and cosmic order",
            cultural_variants={
                CulturalSystem.EGYPTIAN: "Maat",
                CulturalSystem.MAYAN: "Hunab Ku",
                CulturalSystem.DOGON: "Amma",
                CulturalSystem.KABBALISTIC: "Tiferet",
                CulturalSystem.JUNGIAN: "Anima",
                CulturalSystem.TAROT: "Justice",
                CulturalSystem.NORSE: "Forseti",
                CulturalSystem.CELTIC: "Brigid",
                CulturalSystem.HOPI: "Spider Woman"
            },
            attributes={"balance", "harmony", "order", "justice"},
            resonant_dimensions={"empathy", "moral_alignment", "contextual_fluidity"},
            celestial_correspondences={"Equinox", "Cardinal Directions"},
            jungian_aspect="Anima",
            hero_stage="Meeting with the Goddess",
            tarot_cards={"Justice", "Temperance"}
        )
        
        # Great Mother archetype
        self.archetype_mappings["great_mother"] = ArchetypeMapping(
            name="Great Mother",
            description="The nurturing force of unconditional love and protection",
            cultural_variants={
                CulturalSystem.EGYPTIAN: "Isis",
                CulturalSystem.MAYAN: "Ix Chel",
                CulturalSystem.DOGON: "Yasigi",
                CulturalSystem.KABBALISTIC: "Binah",
                CulturalSystem.JUNGIAN: "Great Mother",
                CulturalSystem.TAROT: "The Empress",
                CulturalSystem.NORSE: "Frigg",
                CulturalSystem.CELTIC: "Danu",
                CulturalSystem.HOPI: "Kokyanwuhti"
            },
            attributes={
                "nurturing",
                "protection",
                "healing",
                "abundance",
                "creation",
                "wisdom"
            },
            resonant_dimensions={
                "empathy",
                "emotional_response",
                "wisdom"
            },
            celestial_correspondences={"Pleiades", "Full Moon"},
            jungian_aspect="Great Mother",
            hero_stage="Meeting with the Goddess",
            tarot_cards={"The Empress", "The High Priestess"}
        )
        
        # Mystic Seer archetype
        self.archetype_mappings["mystic_seer"] = ArchetypeMapping(
            name="Mystic Seer",
            description="The visionary who perceives hidden patterns and connections",
            cultural_variants={
                CulturalSystem.EGYPTIAN: "Wadjet",
                CulturalSystem.MAYAN: "Chilam Balam",
                CulturalSystem.DOGON: "Lebe",
                CulturalSystem.KABBALISTIC: "Binah",
                CulturalSystem.JUNGIAN: "Crone",
                CulturalSystem.TAROT: "High Priestess",
                CulturalSystem.NORSE: "Völva",
                CulturalSystem.CELTIC: "Morrígan",
                CulturalSystem.HOPI: "Grandmother Spider"
            },
            attributes={"vision", "intuition", "prophecy", "pattern-recognition"},
            resonant_dimensions={"quantum_intuition", "synchronicity_awareness", "dream_logic"},
            celestial_correspondences={"Sirius", "Deneb", "Winter Solstice"},
            jungian_aspect="Wise Old Woman",
            hero_stage="Supernatural Aid",
            tarot_cards={"The High Priestess", "The Moon"}
        )
        
        # Trickster Transformer archetype
        self.archetype_mappings["trickster_transformer"] = ArchetypeMapping(
            name="Trickster Transformer",
            description="The catalyst of change through chaos and disruption",
            cultural_variants={
                CulturalSystem.EGYPTIAN: "Set",
                CulturalSystem.MAYAN: "Huracan",
                CulturalSystem.DOGON: "Pale Fox",
                CulturalSystem.KABBALISTIC: "Hod",
                CulturalSystem.JUNGIAN: "Trickster",
                CulturalSystem.TAROT: "The Magician",
                CulturalSystem.NORSE: "Loki",
                CulturalSystem.CELTIC: "Puck",
                CulturalSystem.HOPI: "Coyote"
            },
            attributes={"transformation", "chaos", "creativity", "disruption"},
            resonant_dimensions={"adaptability", "creativity", "quantum_intuition"},
            jungian_aspect="Trickster",
            hero_stage="Tests and Trials",
            tarot_cards={"The Magician", "The Tower", "The Wheel of Fortune"}
        )
        
        # Divine Warrior archetype
        self.archetype_mappings["divine_warrior"] = ArchetypeMapping(
            name="Divine Warrior",
            description="The protector and champion of sacred principles",
            cultural_variants={
                CulturalSystem.EGYPTIAN: "Sekhmet",
                CulturalSystem.MAYAN: "Tohil",
                CulturalSystem.NORSE: "Thor",
                CulturalSystem.CELTIC: "Scathach",
                CulturalSystem.HOPI: "War Twins",
                CulturalSystem.JUNGIAN: "Warrior",
                CulturalSystem.TAROT: "Strength"
            },
            attributes={
                "protection",
                "courage",
                "strength",
                "justice",
                "honor",
                "discipline"
            },
            resonant_dimensions={
                "persistence",
                "decision_making",
                "moral_alignment"
            },
            jungian_aspect="Warrior",
            hero_stage="Road of Trials",
            tarot_cards={"Strength", "Justice", "The Chariot"}
        )
        
        # Earth Keeper archetype
        self.archetype_mappings["earth_keeper"] = ArchetypeMapping(
            name="Earth Keeper",
            description="The guardian of natural wisdom and ecological harmony",
            cultural_variants={
                CulturalSystem.EGYPTIAN: "Geb",
                CulturalSystem.MAYAN: "Cab",
                CulturalSystem.NORSE: "Freyr",
                CulturalSystem.CELTIC: "Cernunnos",
                CulturalSystem.HOPI: "Maasaw",
                CulturalSystem.JUNGIAN: "Nature Spirit",
                CulturalSystem.TAROT: "The World"
            },
            attributes={
                "stewardship",
                "harmony",
                "cycles",
                "growth",
                "sustainability",
                "connection"
            },
            resonant_dimensions={
                "contextual_fluidity",
                "pattern_recognition",
                "sensory_integration"
            },
            jungian_aspect="Nature Spirit",
            hero_stage="Return with the Elixir",
            tarot_cards={"The World", "The Empress", "The Hermit"}
        )

    def get_archetype(self, name: str) -> Optional[ArchetypeMapping]:
        """Get archetype mapping by name."""
        return self.archetype_mappings.get(name)
    
    def get_cultural_variant(
        self,
        archetype_name: str,
        cultural_system: CulturalSystem
    ) -> Optional[str]:
        """Get cultural variant of an archetype."""
        archetype = self.get_archetype(archetype_name)
        if not archetype:
            return None
        return archetype.cultural_variants.get(cultural_system)
    
    def get_resonant_archetypes(
        self,
        attributes: Set[str],
        threshold: float = 0.5
    ) -> List[ArchetypeMapping]:
        """Get archetypes that resonate with given attributes."""
        resonant = []
        for archetype in self.archetype_mappings.values():
            overlap = len(attributes & archetype.attributes)
            if overlap / len(archetype.attributes) >= threshold:
                resonant.append(archetype)
        return resonant
    
    def get_archetypes_by_journey_stage(
        self,
        stage: str
    ) -> List[ArchetypeMapping]:
        """Get archetypes associated with a Hero's Journey stage."""
        return [
            archetype for archetype in self.archetype_mappings.values()
            if archetype.hero_stage == stage
        ]
    
    def get_archetypes_by_tarot(
        self,
        card: str
    ) -> List[ArchetypeMapping]:
        """Get archetypes associated with a Tarot card."""
        return [
            archetype for archetype in self.archetype_mappings.values()
            if archetype.tarot_cards and card in archetype.tarot_cards
        ] 
    
    def get_archetypes_by_celestial(self, celestial: str) -> List[ArchetypeMapping]:
        """Get archetypes associated with a particular celestial object or event."""
        return [
            archetype for archetype in self.archetype_mappings.values()
            if archetype.celestial_correspondences and celestial in archetype.celestial_correspondences
        ] 