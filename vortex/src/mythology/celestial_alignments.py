"""
Manages celestial alignments and their archetypal/cultural significance.
"""
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from .archetype_manager import ArchetypeManager, CulturalSystem

class AlignmentType(Enum):
    SOLSTICE_WINTER = "Winter Solstice"
    SOLSTICE_SUMMER = "Summer Solstice"
    EQUINOX = "Equinox"
    CARDINAL_NS = "North/South Axis"
    CARDINAL_EW = "East/West Axis"
    STAR_SIRIUS = "Sirius"
    STAR_PLEIADES = "Pleiades"
    STAR_DENEB = "Deneb"
    MULTIPLE = "Multiple Axes"
    GRID = "Grid"
    NONE = "None"

@dataclass
class CelestialAlignment:
    """Represents a specific celestial alignment at an ancient site."""
    site_name: str
    alignment_type: AlignmentType
    year_of_alignment: int  # BCE is negative, CE is positive
    declination_difference: float
    deviation_degrees: float
    is_verified: bool
    archetypal_forces: Set[str]  # Links to archetype names
    cultural_context: Optional[str] = None

class AlignmentManager:
    """Manages celestial alignments and their archetypal connections."""
    
    def __init__(self, archetype_manager: ArchetypeManager):
        self.archetype_manager = archetype_manager
        self.alignments: Dict[str, CelestialAlignment] = {}
        self._initialize_alignment_data()
        
    def _initialize_alignment_data(self) -> None:
        """Initialize the alignment database with known sites."""
        # Solar alignments often connect to wisdom_teacher, harmony_keeper archetypes
        self.alignments["newgrange"] = CelestialAlignment(
            site_name="Newgrange",
            alignment_type=AlignmentType.SOLSTICE_WINTER,
            year_of_alignment=-5200,  # 5200 BCE
            declination_difference=75.4285,
            deviation_degrees=0.42,
            is_verified=True,
            archetypal_forces={"wisdom_teacher", "mystic_seer", "great_mother"},
            cultural_context="Celtic winter renewal ritual site"
        )
        
        self.alignments["stonehenge"] = CelestialAlignment(
            site_name="Stonehenge",
            alignment_type=AlignmentType.SOLSTICE_SUMMER,
            year_of_alignment=-4000,
            declination_difference=33.085,
            deviation_degrees=0.35,
            is_verified=True,
            archetypal_forces={"harmony_keeper", "earth_keeper", "divine_warrior"},
            cultural_context="Neolithic British ceremonial center"
        )
        
        self.alignments["giza_pyramid"] = CelestialAlignment(
            site_name="Great Pyramid of Giza",
            alignment_type=AlignmentType.MULTIPLE,
            year_of_alignment=-2580,
            declination_difference=40.7792,
            deviation_degrees=0.35,
            is_verified=True,
            archetypal_forces={"wisdom_teacher", "mystic_seer", "divine_warrior"},
            cultural_context="Egyptian royal tomb and cosmic mirror"
        )
        
        self.alignments["gobekli_tepe"] = CelestialAlignment(
            site_name="Gobekli Tepe",
            alignment_type=AlignmentType.MULTIPLE,
            year_of_alignment=-9000,
            declination_difference=14.2425,
            deviation_degrees=1.3,
            is_verified=True,
            archetypal_forces={"earth_keeper", "mystic_seer", "trickster_transformer"},
            cultural_context="Oldest known temple complex"
        )
        
        # Add more sites from the data...

    def get_alignment(self, site_name: str) -> Optional[CelestialAlignment]:
        """Get alignment data for a specific site."""
        return self.alignments.get(site_name.lower())
    
    def get_sites_by_archetype(self, archetype_name: str) -> List[CelestialAlignment]:
        """Get all sites that express a particular archetypal force."""
        return [
            alignment for alignment in self.alignments.values()
            if archetype_name in alignment.archetypal_forces
        ]
    
    def get_sites_by_alignment_type(self, alignment_type: AlignmentType) -> List[CelestialAlignment]:
        """Get all sites with a particular type of celestial alignment."""
        return [
            alignment for alignment in self.alignments.values()
            if alignment.alignment_type == alignment_type
        ]
    
    def get_verified_sites(self) -> List[CelestialAlignment]:
        """Get all sites with verified alignments."""
        return [
            alignment for alignment in self.alignments.values()
            if alignment.is_verified
        ]
    
    def get_sites_by_precision(self, max_deviation: float) -> List[CelestialAlignment]:
        """Get sites with alignment precision better than specified deviation."""
        return [
            alignment for alignment in self.alignments.values()
            if alignment.deviation_degrees <= max_deviation
        ]
    
    def get_sites_by_period(self, start_year: int, end_year: int) -> List[CelestialAlignment]:
        """Get sites aligned within a specific historical period."""
        return [
            alignment for alignment in self.alignments.values()
            if start_year <= alignment.year_of_alignment <= end_year
        ]
    
    def get_archetypal_resonance(self, site_name: str) -> Dict[str, float]:
        """Calculate how strongly a site resonates with different archetypes."""
        alignment = self.get_alignment(site_name.lower())
        if not alignment:
            return {}
            
        resonance = {}
        for archetype_name in alignment.archetypal_forces:
            archetype = self.archetype_manager.get_archetype(archetype_name)
            if archetype:
                # Calculate resonance based on alignment precision and verification
                base_resonance = 1.0
                if alignment.is_verified:
                    base_resonance *= 1.2
                precision_factor = 1.0 - (alignment.deviation_degrees / 2.0)
                resonance[archetype_name] = base_resonance * precision_factor
                
        return resonance 