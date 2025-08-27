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
    AZTEC = "aztec"
    PERSIAN = "persian"
    YORUBA = "yoruba"

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
        self.elemental_mappings: Dict[CulturalSystem, Dict[str, List[str]]] = {}
        self.cosmic_level_mappings: Dict[CulturalSystem, Dict[str, List[str]]] = {}
        self._initialize_core_mappings()
    
    def _initialize_core_mappings(self) -> None:
        """Initialize core archetype mappings across cultures."""
        self.archetype_mappings.update({
            # Creator/Divine Source
            "creator": {
                CulturalSystem.EGYPTIAN: ["ra", "ptah"],
                CulturalSystem.CELTIC: ["dagda", "danu"],
                CulturalSystem.AZTEC: ["ometeotl", "tezcatlipoca"],
                CulturalSystem.PERSIAN: ["ahura_mazda"],
                CulturalSystem.YORUBA: ["olodumare", "olorun"]
            },
            # Wisdom/Knowledge
            "sage": {
                CulturalSystem.EGYPTIAN: ["thoth", "isis"],
                CulturalSystem.CELTIC: ["ogma", "cerridwen"],
                CulturalSystem.AZTEC: ["quetzalcoatl"],
                CulturalSystem.PERSIAN: ["mithra", "anahita"],
                CulturalSystem.YORUBA: ["orunmila", "eshu"]
            },
            # Warrior/Protector
            "warrior": {
                CulturalSystem.EGYPTIAN: ["horus", "sekhmet"],
                CulturalSystem.CELTIC: ["scathach", "cu_chulainn"],
                CulturalSystem.AZTEC: ["huitzilopochtli"],
                CulturalSystem.PERSIAN: ["verethragna"],
                CulturalSystem.YORUBA: ["ogun", "shango"]
            },
            # Mother/Nurturer
            "mother": {
                CulturalSystem.EGYPTIAN: ["isis", "hathor"],
                CulturalSystem.CELTIC: ["brigid", "danu"],
                CulturalSystem.AZTEC: ["coatlicue", "chalchiuhtlicue"],
                CulturalSystem.PERSIAN: ["anahita", "spenta_armaiti"],
                CulturalSystem.YORUBA: ["yemoja", "oshun"]
            },
            # Trickster/Messenger
            "trickster": {
                CulturalSystem.EGYPTIAN: ["set"],
                CulturalSystem.CELTIC: ["gwydion", "lugh"],
                CulturalSystem.AZTEC: ["tezcatlipoca"],
                CulturalSystem.PERSIAN: ["angra_mainyu"],
                CulturalSystem.YORUBA: ["eshu"]
            }
        })

        # Update elemental correspondences
        self.elemental_mappings.update({
            CulturalSystem.EGYPTIAN: {
                "fire": ["ra", "sekhmet"],
                "water": ["osiris", "isis"],
                "air": ["shu", "thoth"],
                "earth": ["geb", "ptah"]
            },
            CulturalSystem.CELTIC: {
                "fire": ["brigid", "lugh"],
                "water": ["manannan", "boann"],
                "air": ["taranis", "morrigan"],
                "earth": ["dagda", "cernunnos"]
            },
            CulturalSystem.AZTEC: {
                "fire": ["xiuhtecuhtli"],
                "water": ["tlaloc", "chalchiuhtlicue"],
                "air": ["ehecatl", "quetzalcoatl"],
                "earth": ["coatlicue", "tlaltecuhtli"]
            },
            CulturalSystem.PERSIAN: {
                "fire": ["atar", "mithra"],
                "water": ["anahita", "tishtrya"],
                "air": ["vayu", "rashnu"],
                "earth": ["spenta_armaiti", "zam"]
            },
            CulturalSystem.YORUBA: {
                "fire": ["shango", "ogun"],
                "water": ["yemoja", "oshun"],
                "air": ["oya", "olorun"],
                "earth": ["onile", "oko"]
            }
        })

        # Update cosmic level associations
        self.cosmic_level_mappings.update({
            CulturalSystem.EGYPTIAN: {
                "celestial": ["ra", "horus"],
                "terrestrial": ["osiris", "isis"],
                "underworld": ["anubis", "nephthys"]
            },
            CulturalSystem.CELTIC: {
                "celestial": ["lugh", "brigid"],
                "terrestrial": ["dagda", "cernunnos"],
                "underworld": ["morrigan", "donn"]
            },
            CulturalSystem.AZTEC: {
                "celestial": ["huitzilopochtli", "tonatiuh"],
                "terrestrial": ["tlaloc", "xipe_totec"],
                "underworld": ["mictlantecuhtli", "mictecacihuatl"]
            },
            CulturalSystem.PERSIAN: {
                "celestial": ["ahura_mazda", "mithra"],
                "terrestrial": ["anahita", "verethragna"],
                "underworld": ["angra_mainyu", "nasu"]
            },
            CulturalSystem.YORUBA: {
                "celestial": ["olodumare", "shango"],
                "terrestrial": ["oshun", "ogun"],
                "underworld": ["eshu", "obaluaye"]
            }
        })

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