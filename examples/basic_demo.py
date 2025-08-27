#!/usr/bin/env python3
"""
Basic Sacred Site Alignment Demo

This script demonstrates the sacred site alignment concepts
without importing from the mythology package to avoid import issues.
It uses direct data examples to show the concept.
"""

from datetime import datetime
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Callable

# ---- Example Enum Classes ----

class CelestialBodyExample(Enum):
    """Example celestial bodies for demonstration."""
    SUN = "sun"
    MOON = "moon"
    MERCURY = "mercury"
    VENUS = "venus"
    PLEIADES = "pleiades"

class AlignmentTypeExample(Enum):
    """Example alignment types for demonstration."""
    SOLSTICE_WINTER = "winter_solstice"
    SOLSTICE_SUMMER = "summer_solstice"
    RISING = "rising"
    SETTING = "setting"
    ZENITH = "zenith"
    CONJUNCTION = "conjunction"

class SiteTypeExample(Enum):
    """Example site types for demonstration."""
    TEMPLE = "temple"
    OBSERVATORY = "observatory"
    KIVA = "kiva"
    ALCHEMICAL_WORKSHOP = "alchemical_workshop"

class CultureTypeExample(Enum):
    """Example culture types for demonstration."""
    SYRIAN_ALCHEMICAL = "syrian_alchemical"
    HOPI = "hopi"

# ---- Example Data Classes ----

@dataclass
class AlignmentMathModelExample:
    """Example mathematical model for calculating alignments."""
    seasonal_variation: float = 0.0
    epoch_shift: float = 0.0
    declination: float = 0.0
    
    def calculate_for_date(self, date: datetime) -> Dict[str, float]:
        """Simplified calculation for a specific date."""
        # This is just a simple example calculation
        day_of_year = date.timetuple().tm_yday
        season_factor = abs(((day_of_year % 183) - 91) / 91)  # 0-1 factor with peaks at solstices
        
        return {
            "azimuth": 90.0 + (self.seasonal_variation * season_factor),
            "altitude": 45.0 + (self.seasonal_variation * season_factor),
            "optimal_time": date.isoformat(),
            "alignment_strength": 0.8 - (0.3 * season_factor)
        }

@dataclass
class CelestialAlignmentExample:
    """Example celestial alignment at a site."""
    alignment_type: AlignmentTypeExample
    primary_body: CelestialBodyExample
    secondary_body: Optional[CelestialBodyExample] = None
    description: str = ""
    cultural_significance: str = ""
    math_model: Optional[AlignmentMathModelExample] = None
    seasonal_variations: Dict[str, str] = field(default_factory=dict)
    
    def calculate_for_date(self, date: datetime) -> Dict[str, float]:
        """Calculate alignment details for a specific date."""
        if self.math_model:
            return self.math_model.calculate_for_date(date)
        else:
            return {"error": "No mathematical model available"}

@dataclass
class SacredSiteExample:
    """Example sacred site with celestial alignments."""
    name: str
    location: Tuple[float, float]  # Latitude, Longitude
    site_type: SiteTypeExample
    culture: CultureTypeExample
    date_range: Tuple[int, int]  # Years BCE/CE (negative for BCE)
    alignments: List[CelestialAlignmentExample]
    description: str
    mythological_connections: Dict[str, str]  # Mythology -> Connection
    
    def calculate_alignments_for_date(self, date: datetime) -> Dict[str, Dict]:
        """Calculate all alignments at this site for a specific date."""
        results = {}
        for alignment in self.alignments:
            key = f"{alignment.alignment_type.value}_{alignment.primary_body.value}"
            if alignment.secondary_body:
                key += f"_{alignment.secondary_body.value}"
            results[key] = alignment.calculate_for_date(date)
        return results

# ---- Example Sacred Sites ----

# Example Syrian alchemical site
HARRAN_EXAMPLE = SacredSiteExample(
    name="Harran Sabians Complex (Example)",
    location=(36.8654, 39.0179),
    site_type=SiteTypeExample.ALCHEMICAL_WORKSHOP,
    culture=CultureTypeExample.SYRIAN_ALCHEMICAL,
    date_range=(500, 900),  # 500-900 CE
    alignments=[
        CelestialAlignmentExample(
            alignment_type=AlignmentTypeExample.RISING,
            primary_body=CelestialBodyExample.MERCURY,
            description="Workshop aligned with Mercury's maximum elongation rising points",
            cultural_significance="Timed alchemical operations related to the Hermetic principles",
            math_model=AlignmentMathModelExample(
                seasonal_variation=5.0,
                epoch_shift=0.1,
                declination=20.0
            ),
            seasonal_variations={
                "spring": "Used for sublimation operations",
                "fall": "Used for coagulation operations"
            }
        ),
        CelestialAlignmentExample(
            alignment_type=AlignmentTypeExample.CONJUNCTION,
            primary_body=CelestialBodyExample.SUN,
            secondary_body=CelestialBodyExample.MOON,
            description="Observatory chambers aligned to track solar-lunar conjunctions",
            cultural_significance="Timing of the Conjunction (Coniunctio) operation in alchemy",
            math_model=AlignmentMathModelExample(
                seasonal_variation=3.0,
                epoch_shift=0.1,
                declination=0.0
            ),
            seasonal_variations={
                "all": "Used to time the 'marriage of opposites' in alchemical work"
            }
        ),
    ],
    description="""
    The Harran complex was a center of Sabian star worship and alchemical practice,
    combining Hellenistic, Persian, and Egyptian influences. The site included observatories,
    alchemical workshops, and temples dedicated to planetary deities.
    """,
    mythological_connections={
        "syrian_alchemical": "Primary center of Hermetic wisdom in the Middle East",
        "egyptian": "Continuation of Alexandrian alchemical traditions",
        "mesopotamian": "Inheritor of Babylonian astronomical traditions"
    }
)

# Example Hopi site
WALPI_EXAMPLE = SacredSiteExample(
    name="Walpi Village (Example)",
    location=(35.8722, -110.5339),
    site_type=SiteTypeExample.KIVA,
    culture=CultureTypeExample.HOPI,
    date_range=(1100, 1900),
    alignments=[
        CelestialAlignmentExample(
            alignment_type=AlignmentTypeExample.SOLSTICE_WINTER,
            primary_body=CelestialBodyExample.SUN,
            description="Kiva sipapu and fire pit aligned with winter solstice sunrise",
            cultural_significance="Timing of Soyal ceremony and beginning of the ceremonial cycle",
            math_model=AlignmentMathModelExample(
                seasonal_variation=3.0,
                epoch_shift=0.15,
                declination=-23.5
            ),
            seasonal_variations={
                "winter": "Marks the return of the Sun and beginning of Kachina season"
            }
        ),
        CelestialAlignmentExample(
            alignment_type=AlignmentTypeExample.RISING,
            primary_body=CelestialBodyExample.PLEIADES,
            description="Village orientation aligned with Pleiades rising in June",
            cultural_significance="Associated with agricultural cycles and world emergence",
            math_model=AlignmentMathModelExample(
                seasonal_variation=1.0,
                epoch_shift=0.3,
                declination=24.0
            ),
            seasonal_variations={
                "summer": "Used to time planting and certain ceremonies"
            }
        )
    ],
    description="""
    Walpi is one of the oldest continuously inhabited villages in North America, 
    situated on First Mesa in the Hopi territory. The village layout and kiva 
    structures incorporate precise astronomical alignments used for ceremony timing.
    """,
    mythological_connections={
        "hopi": "Connection to Emergence narrative and world cycles",
        "pueblo": "Shared ceremonial traditions with other Pueblo peoples",
        "navajo": "Interactions and shared cosmological elements"
    }
)

# Collection of example sacred sites
EXAMPLE_SITES = {
    "harran": HARRAN_EXAMPLE,
    "walpi": WALPI_EXAMPLE
}

# ---- Demo Functions ----

def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_json(data: Dict) -> None:
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2, default=str))

def show_site_info(site: SacredSiteExample) -> None:
    """Display basic information about a sacred site."""
    print(f"Site: {site.name}")
    print(f"Culture: {site.culture.value}")
    print(f"Location: {site.location}")
    print(f"Date Range: {site.date_range}")
    print("\nAlignments:")
    
    for alignment in site.alignments:
        print(f"  - {alignment.alignment_type.value} of {alignment.primary_body.value}")
        if alignment.secondary_body:
            print(f"    with {alignment.secondary_body.value}")
        print(f"    Significance: {alignment.cultural_significance}")
    
    print("\nMythological Connections:")
    for mythology, connection in site.mythological_connections.items():
        print(f"  - {mythology}: {connection}")

def calculate_alignments(site: SacredSiteExample, date: datetime) -> None:
    """Calculate alignments for a site on a specific date."""
    alignments = site.calculate_alignments_for_date(date)
    print(f"\nAlignments for {site.name} on {date.date()}:")
    print_json(alignments)

def analyze_site_alignments(site: SacredSiteExample) -> None:
    """Analyze alignments for a site."""
    print_section(f"ALIGNMENT ANALYSIS FOR {site.name.upper()}")
    
    # Show all alignments
    print("Alignments:")
    for idx, alignment in enumerate(site.alignments, 1):
        print(f"{idx}. {alignment.alignment_type.value} of {alignment.primary_body.value}")
        if alignment.secondary_body:
            print(f"   with {alignment.secondary_body.value}")
        print(f"   Significance: {alignment.cultural_significance}")
        
        # Show seasonal variations if available
        if alignment.seasonal_variations:
            print("   Seasonal Variations:")
            for season, description in alignment.seasonal_variations.items():
                print(f"     - {season.capitalize()}: {description}")
        
        # Show mathematical model if available
        if alignment.math_model:
            print("   Has mathematical model: Yes")
            print(f"     Seasonal variation: {alignment.math_model.seasonal_variation} degrees")
            print(f"     Epoch shift: {alignment.math_model.epoch_shift} degrees/century")
        else:
            print("   Has mathematical model: No")
        
        print()

def calculate_alignment_for_dates(site: SacredSiteExample) -> None:
    """Calculate alignments for key dates."""
    print_section(f"ALIGNMENT CALCULATIONS FOR {site.name.upper()}")
    
    # Key astronomical dates in 2023
    dates = [
        datetime(2023, 12, 21),  # Winter solstice
        datetime(2023, 6, 21),   # Summer solstice
        datetime(2023, 3, 20),   # Spring equinox
        datetime(2023, 9, 22),   # Fall equinox
        datetime.now()           # Current date
    ]
    
    for date in dates:
        calculate_alignments(site, date)
        print("\n" + "-" * 40 + "\n")

def run_demo() -> None:
    """Run the complete demonstration."""
    print_section("SACRED SITE ALIGNMENT DEMONSTRATION")
    print("This script demonstrates the sacred site alignment concept using example data.")
    
    # Show sites
    print_section("EXAMPLE SACRED SITES")
    print(f"Found {len(EXAMPLE_SITES)} example sacred sites:")
    for site_id, site in EXAMPLE_SITES.items():
        print(f"- {site.name} ({site.site_type.value})")
        print(f"  Location: {site.location}")
        print(f"  Date Range: {site.date_range}")
        print(f"  Number of alignments: {len(site.alignments)}")
        print()
    
    # Show detailed information for sites
    print_section("DETAILED SITE INFORMATION")
    
    show_site_info(HARRAN_EXAMPLE)
    print("\n" + "-" * 40 + "\n")
    show_site_info(WALPI_EXAMPLE)
    
    # Analyze alignments for both sites
    analyze_site_alignments(HARRAN_EXAMPLE)
    analyze_site_alignments(WALPI_EXAMPLE)
    
    # Calculate alignments for key dates
    calculate_alignment_for_dates(HARRAN_EXAMPLE)
    calculate_alignment_for_dates(WALPI_EXAMPLE)
    
    print_section("DEMONSTRATION COMPLETED")
    print("The sacred site alignment concept has been successfully demonstrated.")
    print("In the actual implementation, these calculations would be more sophisticated")
    print("and would incorporate real astronomical data and historical information.")

if __name__ == "__main__":
    run_demo() 