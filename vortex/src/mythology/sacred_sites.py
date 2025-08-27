"""
Sacred Sites and Their Celestial Alignments

This module catalogs sacred sites across different mythological traditions,
their astronomical alignments, and cultural significance. It provides tools
for analyzing and comparing these alignments across different cultures.
"""

from typing import Dict, List, Optional, Set, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import math

from .celestial_alignments import CelestialBody, AlignmentType
# Import the Syrian and Hopi specific information
from .syrian import AlchemicalStage, AlchemicalElement
from .hopi import Direction, WorldCycle

class SiteType(Enum):
    """Types of sacred sites."""
    TEMPLE = "temple"
    PYRAMID = "pyramid"
    OBSERVATORY = "observatory"
    CITY = "city"
    STONE_CIRCLE = "stone_circle"
    BURIAL_MOUND = "burial_mound"
    CAVE = "cave"
    MOUNTAIN = "mountain"
    COMPLEX = "complex"
    ALCHEMICAL_WORKSHOP = "alchemical_workshop"
    KIVA = "kiva"

class CultureType(Enum):
    """Cultural traditions associated with sacred sites."""
    MAYAN = "mayan"
    AZTEC = "aztec"
    EGYPTIAN = "egyptian"
    CELTIC = "celtic"
    MESOPOTAMIAN = "mesopotamian"
    GRECO_ROMAN = "greco_roman"
    HINDU = "hindu"
    KHMER = "khmer"
    NEOLITHIC_EUROPEAN = "neolithic_european"
    INCAN = "incan"
    HOPI = "hopi"
    SYRIAN_ALCHEMICAL = "syrian_alchemical"
    CHINESE = "chinese"
    JAPANESE = "japanese"
    DOGON = "dogon"

@dataclass
class AlignmentMathModel:
    """Mathematical model for calculating precise alignments based on date and time."""
    formula: Callable[[datetime, float, float], Tuple[float, float]]  # Function that calculates azimuth and altitude
    seasonal_variation: float = 0.0  # Degrees of variation throughout the year
    epoch_shift: float = 0.0  # Degrees of shift per century due to precession
    declination_parameters: Dict[str, float] = field(default_factory=dict)  # Parameters for declination calculations
    
    def calculate_alignment(self, date: datetime, latitude: float, longitude: float) -> Tuple[float, float]:
        """Calculate the precise alignment for a given date and location."""
        return self.formula(date, latitude, longitude)
    
    def calculate_optimal_viewing_time(self, date: datetime, latitude: float, longitude: float) -> datetime:
        """Calculate the optimal time to observe the alignment on a given date."""
        # Default implementation uses noon as the baseline, adjusted by seasonal factors
        base_time = datetime(date.year, date.month, date.day, 12, 0, 0)
        
        # Adjust based on seasonal variation
        day_of_year = date.timetuple().tm_yday
        seasonal_adjustment = self.seasonal_variation * math.sin((day_of_year / 365) * 2 * math.pi)
        
        # Convert degrees to hours (15 degrees = 1 hour)
        hour_adjustment = seasonal_adjustment / 15
        
        # Apply adjustment
        return base_time + timedelta(hours=hour_adjustment)

@dataclass
class CelestialAlignment:
    """A specific celestial alignment at a site."""
    alignment_type: AlignmentType
    primary_body: CelestialBody
    secondary_body: Optional[CelestialBody] = None
    date_range: Optional[Tuple[int, int]] = None  # Years BCE/CE when alignment was valid
    angle: Optional[float] = None  # Degrees
    solstice_equinox: Optional[str] = None
    description: Optional[str] = None
    cultural_significance: Optional[str] = None
    math_model: Optional[AlignmentMathModel] = None  # Mathematical model for precise calculations
    seasonal_variations: Dict[str, str] = field(default_factory=dict)  # Season -> Description of variation
    
    def calculate_for_date(self, date: datetime, latitude: float, longitude: float) -> Dict[str, float]:
        """Calculate precise alignment details for a specific date."""
        if not self.math_model:
            return {"error": "No mathematical model available for this alignment"}
            
        azimuth, altitude = self.math_model.calculate_alignment(date, latitude, longitude)
        optimal_time = self.math_model.calculate_optimal_viewing_time(date, latitude, longitude)
        
        return {
            "azimuth": azimuth,
            "altitude": altitude,
            "optimal_time": optimal_time.isoformat(),
            "is_visible": altitude > 0,
            "alignment_strength": self._calculate_alignment_strength(azimuth, altitude, date)
        }
    
    def _calculate_alignment_strength(self, azimuth: float, altitude: float, date: datetime) -> float:
        """Calculate the strength or accuracy of the alignment (0.0-1.0)."""
        # Base strength starts at 1.0 (perfect)
        strength = 1.0
        
        # If we have a specific angle to compare against
        if self.angle is not None:
            angle_diff = abs(self.angle - azimuth) % 360
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
            
            # Reduce strength based on angular difference (5 degrees = 0.5 reduction)
            strength -= min(1.0, angle_diff / 10)
        
        # Adjust for date if we have a date range
        if self.date_range is not None:
            current_year = date.year
            if current_year < self.date_range[0] or current_year > self.date_range[1]:
                # Outside the date range, strength reduced
                strength *= 0.5
        
        # Ensure strength is between 0 and 1
        return max(0.0, min(1.0, strength))

@dataclass
class SacredSite:
    """Information about a sacred site and its celestial alignments."""
    name: str
    location: Tuple[float, float]  # Latitude, Longitude
    site_type: SiteType
    culture: CultureType
    date_range: Tuple[int, int]  # Years BCE/CE (negative for BCE)
    alignments: List[CelestialAlignment]
    description: str
    mythological_connections: Dict[str, str]  # Mythology -> Connection
    zenith_passages: Optional[List[CelestialBody]] = None  # Bodies that pass directly overhead
    cultural_elements: Dict[str, List[str]] = field(default_factory=dict)  # Element type -> list of elements
    
    def get_alignments_by_type(self, alignment_type: AlignmentType) -> List[CelestialAlignment]:
        """Get all alignments of a specific type at this site."""
        return [a for a in self.alignments if a.alignment_type == alignment_type]
    
    def get_alignments_by_body(self, body: CelestialBody) -> List[CelestialAlignment]:
        """Get all alignments involving a specific celestial body at this site."""
        return [a for a in self.alignments if a.primary_body == body or a.secondary_body == body]
    
    def calculate_alignments_for_date(self, date: datetime) -> Dict[str, Dict[str, float]]:
        """Calculate all alignments at this site for a specific date."""
        results = {}
        for alignment in self.alignments:
            if alignment.math_model:
                alignment_key = f"{alignment.alignment_type.value}_{alignment.primary_body.value}"
                if alignment.secondary_body:
                    alignment_key += f"_{alignment.secondary_body.value}"
                results[alignment_key] = alignment.calculate_for_date(date, self.location[0], self.location[1])
        return results

# Mathematical models for common alignments
def _solstice_formula(date: datetime, latitude: float, longitude: float) -> Tuple[float, float]:
    """Calculate the sunrise azimuth and altitude for solstices."""
    # Simplified calculation for demonstration
    day_of_year = date.timetuple().tm_yday
    
    # Approximate declination of the Sun at solstices
    if 355 <= day_of_year or day_of_year <= 10:  # Winter solstice (Northern Hemisphere)
        declination = -23.44
    elif 170 <= day_of_year <= 190:  # Summer solstice (Northern Hemisphere)
        declination = 23.44
    else:
        # Interpolate between solstices
        if day_of_year < 170:
            progress = day_of_year / 170
            declination = -23.44 + (46.88 * progress)
        else:
            progress = (day_of_year - 190) / 165
            declination = 23.44 - (46.88 * progress)
    
    # Convert to radians
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)
    
    # Calculate sunrise azimuth
    cos_az = (math.sin(dec_rad) - math.sin(lat_rad) * math.sin(0)) / (math.cos(lat_rad) * math.cos(0))
    azimuth = math.degrees(math.acos(max(-1, min(1, cos_az))))
    
    # Adjust for hemisphere
    if date.month >= 3 and date.month <= 9:
        azimuth = 360 - azimuth
    
    # Sunrise altitude is 0 by definition, but affected by atmospheric refraction
    altitude = 0.0
    
    return azimuth, altitude

def _equinox_formula(date: datetime, latitude: float, longitude: float) -> Tuple[float, float]:
    """Calculate the sunrise azimuth and altitude for equinoxes."""
    # At equinoxes, the sun rises due east
    return 90.0, 0.0

# Syrian alchemical workshop solar alignment model
def _syrian_alchemical_formula(date: datetime, latitude: float, longitude: float) -> Tuple[float, float]:
    """Calculate the solar alignment for Syrian alchemical workshops at key operational times."""
    # Alchemical operations were often timed to specific solar positions
    hour = date.hour
    month = date.month
    
    # Different operations had different ideal solar positions
    if 4 <= month <= 9:  # Spring/Summer - Calcination (Solar zenith)
        if 10 <= hour <= 14:
            altitude = 75.0 - abs(latitude - 34.0)  # Maximum altitude, adjusted for latitude difference from Damascus
            azimuth = 180.0  # Due south
        else:
            altitude = 45.0
            azimuth = 135.0 if hour < 12 else 225.0
    else:  # Fall/Winter - Dissolution (Lower sun)
        if 10 <= hour <= 14:
            altitude = 45.0 - abs(latitude - 34.0)
            azimuth = 180.0
        else:
            altitude = 30.0
            azimuth = 135.0 if hour < 12 else 225.0
    
    return azimuth, altitude

# Hopi kiva alignment model
def _hopi_kiva_formula(date: datetime, latitude: float, longitude: float) -> Tuple[float, float]:
    """Calculate alignments for Hopi kivas based on solar and stellar positions."""
    month = date.month
    day = date.day
    
    # Winter solstice alignment (December 21)
    if month == 12 and 20 <= day <= 22:
        return 125.0, 0.0  # Sunrise azimuth at winter solstice
    
    # Summer solstice alignment (June 21)
    elif month == 6 and 20 <= day <= 22:
        return 65.0, 0.0  # Sunrise azimuth at summer solstice
    
    # Pleiades rising (important for certain ceremonies)
    elif month == 6 and 1 <= day <= 15:
        return 65.0, 15.0  # Pleiades rising in early June
    
    # Default value for other times
    else:
        # East-facing alignment common in many kivas
        return 90.0, 10.0

# Common mathematical models
SOLSTICE_MODEL = AlignmentMathModel(
    formula=_solstice_formula,
    seasonal_variation=1.5,
    epoch_shift=0.2,
    declination_parameters={"max_declination": 23.44}
)

EQUINOX_MODEL = AlignmentMathModel(
    formula=_equinox_formula,
    seasonal_variation=0.5,
    epoch_shift=0.0,
    declination_parameters={"declination": 0.0}
)

SYRIAN_ALCHEMICAL_MODEL = AlignmentMathModel(
    formula=_syrian_alchemical_formula,
    seasonal_variation=5.0,
    epoch_shift=0.1,
    declination_parameters={"reference_latitude": 34.0}  # Damascus latitude
)

HOPI_KIVA_MODEL = AlignmentMathModel(
    formula=_hopi_kiva_formula,
    seasonal_variation=3.0,
    epoch_shift=0.15,
    declination_parameters={"reference_latitude": 36.0}  # Hopi mesas latitude
)

# Major sacred sites and their celestial alignments
SACRED_SITES = {
    "teotihuacan": SacredSite(
        name="Teotihuacan",
        location=(19.6925, -98.8438),
        site_type=SiteType.CITY,
        culture=CultureType.AZTEC,
        date_range=(-100, 750),  # ~100 BCE to 750 CE
        alignments=[
            CelestialAlignment(
                alignment_type=AlignmentType.ZENITH,
                primary_body=CelestialBody.SUN,
                date_range=(1, 750),
                description="Sun passes directly overhead on May 19 and July 25",
                cultural_significance="Marks key points in agricultural calendar and ritual cycle",
                math_model=AlignmentMathModel(
                    formula=lambda d, lat, lon: (180.0, 90.0) if (d.month == 5 and d.day == 19) or (d.month == 7 and d.day == 25) else (180.0, 75.0),
                    seasonal_variation=0.0,
                    epoch_shift=0.0
                ),
                seasonal_variations={
                    "spring": "Used to time maize planting rituals",
                    "summer": "Used to determine harvest preparations",
                    "fall": "Used to calculate festival timing",
                    "winter": "Used for ceremonial planning for next year"
                }
            ),
            CelestialAlignment(
                alignment_type=AlignmentType.RISING,
                primary_body=CelestialBody.PLEIADES,
                date_range=(1, 750),
                description="City grid aligned to Pleiades rising on specific dates",
                cultural_significance="Connected to creation mythology and calendar system",
                math_model=AlignmentMathModel(
                    formula=lambda d, lat, lon: (65.0, 0.0) if (d.month == 6) else (70.0, 0.0),
                    seasonal_variation=2.0,
                    epoch_shift=0.3
                )
            ),
        ],
        description="""
        Teotihuacan was one of the largest cities in the pre-Columbian Americas, 
        with significant religious and cultural influence. Its name means "place where 
        gods were born" in Nahuatl. The city is characterized by the massive Pyramid of the 
        Sun, Pyramid of the Moon, and the Avenue of the Dead. The entire city shows precise 
        astronomical alignments in its layout.
        """,
        mythological_connections={
            "aztec": "Place of creation of the current sun and moon",
            "mayan": "Connected to Venus and celestial origin myths"
        },
        zenith_passages=[CelestialBody.SUN]
    ),
    
    "pyramids_giza": SacredSite(
        name="Great Pyramids of Giza",
        location=(29.9792, 31.1342),
        site_type=SiteType.PYRAMID,
        culture=CultureType.EGYPTIAN,
        date_range=(-2580, -2480),
        alignments=[
            CelestialAlignment(
                alignment_type=AlignmentType.MULTIPLE,
                primary_body=CelestialBody.ORION,
                description="Alignment of the three pyramids with Orion's Belt",
                cultural_significance="Connected to Osiris and afterlife mythology",
                math_model=AlignmentMathModel(
                    formula=lambda d, lat, lon: (180.0, 45.0),
                    seasonal_variation=0.0,
                    epoch_shift=0.5
                ),
                seasonal_variations={
                    "winter": "Most visible during clear winter nights"
                }
            ),
            CelestialAlignment(
                alignment_type=AlignmentType.RISING,
                primary_body=CelestialBody.SIRIUS,
                date_range=(-2580, -2480),
                description="Aligned with the rising of Sirius, the brightest star",
                cultural_significance="Heralded the Nile flooding and new year",
                math_model=AlignmentMathModel(
                    formula=lambda d, lat, lon: (110.0, 0.0),
                    seasonal_variation=1.0,
                    epoch_shift=0.8
                ),
                seasonal_variations={
                    "summer": "Heliacal rising coincided with Nile floods"
                }
            ),
        ],
        description="""
        The Pyramids of Giza are among the most iconic ancient structures, built as 
        tombs for the pharaohs Khufu, Khafre, and Menkaure. Their precise alignment 
        with cardinal directions and celestial bodies demonstrates advanced astronomical 
        knowledge. The Great Pyramid's internal shafts align with key stars that were 
        significant in Egyptian mythology.
        """,
        mythological_connections={
            "egyptian": "Journey of the pharaoh to the celestial realm",
            "syrian_alchemical": "Material embodiment of celestial principles"
        },
        cultural_elements={
            "alchemical_principle": ["transference", "perfection", "immortality"],
            "elements": ["earth", "air", "fire", "water"]
        }
    ),
    
    "stonehenge": SacredSite(
        name="Stonehenge",
        location=(51.1789, -1.8262),
        site_type=SiteType.STONE_CIRCLE,
        culture=CultureType.NEOLITHIC_EUROPEAN,
        date_range=(-3000, -1500),
        alignments=[
            CelestialAlignment(
                alignment_type=AlignmentType.SOLSTICE_SUMMER,
                primary_body=CelestialBody.SUN,
                description="Main axis aligned with summer solstice sunrise",
                cultural_significance="Marked turning point of the year and fertility cycles",
                math_model=SOLSTICE_MODEL,
                seasonal_variations={
                    "summer": "Alignment visible at sunrise on summer solstice"
                }
            ),
            CelestialAlignment(
                alignment_type=AlignmentType.SOLSTICE_WINTER,
                primary_body=CelestialBody.SUN,
                description="Aligned with winter solstice sunset",
                cultural_significance="Rebirth of the sun after shortest day",
                math_model=SOLSTICE_MODEL,
                seasonal_variations={
                    "winter": "Alignment visible at sunset on winter solstice"
                }
            ),
        ],
        description="""
        Stonehenge is a prehistoric monument consisting of standing stones arranged 
        in concentric rings. Built in several stages, it demonstrates remarkable 
        astronomical knowledge, particularly related to solar and lunar cycles.
        The site was likely used for ritual ceremonies and as a calendrical device.
        """,
        mythological_connections={
            "celtic": "Sacred gathering place at key solar turning points",
            "neolithic": "Possible ancestor worship and fertility rituals"
        }
    ),
    
    # Additional entries for Syrian Alchemical and Hopi sites
    "harran_sabians": SacredSite(
        name="Harran Sabians Complex",
        location=(36.8654, 39.0179),
        site_type=SiteType.ALCHEMICAL_WORKSHOP,
        culture=CultureType.SYRIAN_ALCHEMICAL,
        date_range=(500, 900),  # 500-900 CE
        alignments=[
            CelestialAlignment(
                alignment_type=AlignmentType.RISING,
                primary_body=CelestialBody.MERCURY,
                description="Workshop aligned with Mercury's maximum elongation rising points",
                cultural_significance="Timed alchemical operations related to the Hermetic principles",
                math_model=SYRIAN_ALCHEMICAL_MODEL,
                seasonal_variations={
                    "spring": "Used for sublimation operations",
                    "fall": "Used for coagulation operations"
                }
            ),
            CelestialAlignment(
                alignment_type=AlignmentType.CONJUNCTION,
                primary_body=CelestialBody.SUN,
                secondary_body=CelestialBody.MOON,
                description="Observatory chambers aligned to track solar-lunar conjunctions",
                cultural_significance="Timing of the Conjunction (Coniunctio) operation in alchemy",
                math_model=AlignmentMathModel(
                    formula=lambda d, lat, lon: (90.0, 45.0),
                    seasonal_variation=3.0,
                    epoch_shift=0.1
                ),
                seasonal_variations={
                    "all": "Used to time the 'marriage of opposites' in alchemical work"
                }
            ),
        ],
        description="""
        The Harran complex was a center of Sabian star worship and alchemical practice,
        combining Hellenistic, Persian, and Egyptian influences. The site included observatories,
        alchemical workshops, and temples dedicated to planetary deities. The Sabians of Harran
        were known for their astronomical knowledge and preservation of Hermetic texts.
        """,
        mythological_connections={
            "syrian_alchemical": "Primary center of Hermetic wisdom in the Middle East",
            "egyptian": "Continuation of Alexandrian alchemical traditions",
            "mesopotamian": "Inheritor of Babylonian astronomical traditions"
        },
        cultural_elements={
            "alchemical_stage": [AlchemicalStage.MELANOSIS.value, AlchemicalStage.LEUKOSIS.value,
                                AlchemicalStage.XANTHOSIS.value, AlchemicalStage.IOSIS.value],
            "alchemical_element": [AlchemicalElement.MERCURY.value, AlchemicalElement.SULFUR.value]
        }
    ),
    
    "aleppo_citadel": SacredSite(
        name="Aleppo Citadel Alchemical Chambers",
        location=(36.1994, 37.1597),
        site_type=SiteType.ALCHEMICAL_WORKSHOP,
        culture=CultureType.SYRIAN_ALCHEMICAL,
        date_range=(900, 1200),
        alignments=[
            CelestialAlignment(
                alignment_type=AlignmentType.SOLSTICE_SUMMER,
                primary_body=CelestialBody.SUN,
                description="Roof opening aligned with summer solstice zenith",
                cultural_significance="Timed calcination operations at maximum solar power",
                math_model=SYRIAN_ALCHEMICAL_MODEL,
                seasonal_variations={
                    "summer": "Used for calcination at maximum solar intensity"
                }
            ),
            CelestialAlignment(
                alignment_type=AlignmentType.RISING,
                primary_body=CelestialBody.VENUS,
                description="Eastern window aligned with Venus morning star rising",
                cultural_significance="Associated with the White Stage (Albedo) of the Great Work",
                math_model=AlignmentMathModel(
                    formula=lambda d, lat, lon: (77.0, 0.0),
                    seasonal_variation=2.0,
                    epoch_shift=0.2
                ),
                seasonal_variations={
                    "spring": "Venus morning star appearances timed purification rituals"
                }
            )
        ],
        description="""
        The hidden alchemical chambers within Aleppo Citadel were constructed to harness
        specific celestial energies for alchemical operations. The workshops featured
        sophisticated vent systems, solar alignments, and specialized areas for different
        stages of the Great Work. These chambers represent a sophisticated integration of
        architectural design with alchemical and astronomical knowledge.
        """,
        mythological_connections={
            "syrian_alchemical": "Chambers dedicated to the Great Work of transmutation",
            "greek": "Incorporated Aristotelian elemental philosophy",
            "persian": "Integrated Zoroastrian fire symbolism"
        },
        cultural_elements={
            "alchemical_stage": [AlchemicalStage.LEUKOSIS.value, AlchemicalStage.IOSIS.value],
            "alchemical_element": [AlchemicalElement.SALT.value, AlchemicalElement.FIRE.value,
                                  AlchemicalElement.QUINTESSENCE.value]
        }
    ),
    
    "walpi_village": SacredSite(
        name="Walpi Village",
        location=(35.8722, -110.5339),
        site_type=SiteType.KIVA,
        culture=CultureType.HOPI,
        date_range=(1100, 1900),
        alignments=[
            CelestialAlignment(
                alignment_type=AlignmentType.SOLSTICE_WINTER,
                primary_body=CelestialBody.SUN,
                description="Kiva sipapu and fire pit aligned with winter solstice sunrise",
                cultural_significance="Timing of Soyal ceremony and beginning of the ceremonial cycle",
                math_model=HOPI_KIVA_MODEL,
                seasonal_variations={
                    "winter": "Marks the return of the Sun and beginning of Kachina season"
                }
            ),
            CelestialAlignment(
                alignment_type=AlignmentType.RISING,
                primary_body=CelestialBody.PLEIADES,
                description="Village orientation aligned with Pleiades rising in June",
                cultural_significance="Associated with agricultural cycles and world emergence",
                math_model=AlignmentMathModel(
                    formula=lambda d, lat, lon: (65.0, 15.0) if d.month == 6 else (65.0, 10.0),
                    seasonal_variation=1.0,
                    epoch_shift=0.3
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
        The integration of celestial knowledge with architectural and ceremonial practices
        demonstrates the sophisticated astronomical traditions of the Hopi people.
        """,
        mythological_connections={
            "hopi": "Connection to Emergence narrative and world cycles",
            "pueblo": "Shared ceremonial traditions with other Pueblo peoples",
            "navajo": "Interactions and shared cosmological elements"
        },
        cultural_elements={
            "direction": [Direction.EAST.value, Direction.WEST.value, Direction.ABOVE.value],
            "world_cycle": [WorldCycle.TUWAQACHI.value]
        }
    ),
    
    "shungopavi_kiva": SacredSite(
        name="Shungopavi Snake Kiva",
        location=(35.8831, -110.5903),
        site_type=SiteType.KIVA,
        culture=CultureType.HOPI,
        date_range=(1200, 1950),
        alignments=[
            CelestialAlignment(
                alignment_type=AlignmentType.ZENITH,
                primary_body=CelestialBody.SUN,
                description="Central roof opening aligned with solar zenith passage in August",
                cultural_significance="Timing of Snake-Antelope ceremonies for rain bringing",
                math_model=HOPI_KIVA_MODEL,
                seasonal_variations={
                    "summer": "Used for rain-bringing ceremonies during dry season"
                }
            ),
            CelestialAlignment(
                alignment_type=AlignmentType.SOLSTICE_SUMMER,
                primary_body=CelestialBody.SUN,
                description="Eastern wall aligned with summer solstice sunrise",
                cultural_significance="Timing of Niman Kachina ceremony",
                math_model=SOLSTICE_MODEL,
                seasonal_variations={
                    "summer": "Marks the departure of kachinas to their home in the San Francisco Peaks"
                }
            )
        ],
        description="""
        The Shungopavi Snake Kiva is a specialized ceremonial structure used for
        the famous Snake Dance and related rituals. It incorporates precise solar
        alignments that help time these important ceremonies, which are performed
        to bring rain during the crucial agricultural season. The structure demonstrates
        how architectural design, ceremony, and astronomical knowledge are integrated
        in Hopi cultural practice.
        """,
        mythological_connections={
            "hopi": "Site of Snake-Antelope ceremonies for rain-bringing",
            "zuni": "Related rain ceremony practices"
        },
        zenith_passages=[CelestialBody.SUN],
        cultural_elements={
            "direction": [Direction.SOUTH.value, Direction.BELOW.value],
            "world_cycle": [WorldCycle.TOKPA.value, WorldCycle.TUWAQACHI.value]
        }
    )
}

def get_site_by_name(name: str) -> Optional[SacredSite]:
    """Retrieve a sacred site by its name."""
    for site_key, site in SACRED_SITES.items():
        if site.name.lower() == name.lower():
            return site
    return None

def get_sites_by_culture(culture: CultureType) -> List[SacredSite]:
    """Get all sacred sites associated with a specific culture."""
    return [site for site in SACRED_SITES.values() if site.culture == culture]

def get_sites_by_alignment(alignment_type: AlignmentType, celestial_body: CelestialBody) -> List[SacredSite]:
    """Find sites that have a specific type of celestial alignment."""
    matching_sites = []
    
    for site in SACRED_SITES.values():
        for alignment in site.alignments:
            if (alignment.alignment_type == alignment_type and 
                (alignment.primary_body == celestial_body or alignment.secondary_body == celestial_body)):
                matching_sites.append(site)
                break
    
    return matching_sites

def get_sites_with_zenith_passages() -> List[SacredSite]:
    """Get all sites with zenith passages of celestial bodies."""
    return [site for site in SACRED_SITES.values() if site.zenith_passages]

def find_mythological_connections(mythology: str) -> Dict[str, str]:
    """Find all sites with connections to a specific mythology."""
    connections = {}
    
    for site_key, site in SACRED_SITES.values():
        if mythology in site.mythological_connections:
            connections[site.name] = site.mythological_connections[mythology]
    
    return connections

def calculate_solar_position(date: datetime, latitude: float, longitude: float) -> Dict[str, float]:
    """Calculate the position of the sun for a given date and location."""
    # This is a simplified calculation for demonstration purposes
    day_of_year = date.timetuple().tm_yday
    hour = date.hour + date.minute / 60
    
    # Declination of the sun (simplified)
    declination = 23.45 * math.sin(math.radians((360/365) * (day_of_year - 81)))
    
    # Hour angle
    hour_angle = 15 * (hour - 12)
    
    # Convert to radians
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)
    hour_rad = math.radians(hour_angle)
    
    # Altitude
    sin_alt = math.sin(lat_rad) * math.sin(dec_rad) + math.cos(lat_rad) * math.cos(dec_rad) * math.cos(hour_rad)
    altitude = math.degrees(math.asin(sin_alt))
    
    # Azimuth
    cos_az = (math.sin(dec_rad) - math.sin(lat_rad) * math.sin(math.radians(altitude))) / (math.cos(lat_rad) * math.cos(math.radians(altitude)))
    azimuth = math.degrees(math.acos(max(-1, min(1, cos_az))))
    
    # Adjust azimuth for afternoon
    if hour_angle > 0:
        azimuth = 360 - azimuth
    
    return {
        "azimuth": azimuth,
        "altitude": altitude,
        "declination": declination
    }

def does_polaris_cross_zenith(site: SacredSite) -> bool:
    """Determine if Polaris crosses the zenith at a sacred site."""
    latitude = site.location[0]
    
    # Simplified check - Polaris is at approximately 89.3° declination
    # It crosses the zenith when site latitude is very close to 89.3° North
    return abs(latitude - 89.3) < 1.0

def get_alignment_seasonal_variation(site_name: str, alignment_type: AlignmentType, body: CelestialBody) -> Dict[str, str]:
    """Get the seasonal variations of a specific alignment at a site."""
    site = get_site_by_name(site_name)
    if not site:
        return {"error": "Site not found"}
    
    for alignment in site.alignments:
        if alignment.alignment_type == alignment_type and alignment.primary_body == body:
            return alignment.seasonal_variations
    
    return {"error": "Alignment not found at this site"}

def calculate_site_alignments_for_date(site_name: str, date: datetime) -> Dict:
    """Calculate all alignments at a site for a specific date."""
    site = get_site_by_name(site_name)
    if not site:
        return {"error": "Site not found"}
    
    return {
        "site": site.name,
        "date": date.isoformat(),
        "alignments": site.calculate_alignments_for_date(date)
    }

def get_syrian_alchemical_sites() -> List[SacredSite]:
    """Get all sites associated with Syrian alchemical traditions."""
    return get_sites_by_culture(CultureType.SYRIAN_ALCHEMICAL)

def get_hopi_sites() -> List[SacredSite]:
    """Get all sites associated with Hopi traditions."""
    return get_sites_by_culture(CultureType.HOPI)

def get_alchemical_elements_at_sites() -> Dict[str, List[str]]:
    """Get alchemical elements associated with different sites."""
    elements_by_site = {}
    
    for site_key, site in SACRED_SITES.items():
        if "alchemical_element" in site.cultural_elements:
            elements_by_site[site.name] = site.cultural_elements["alchemical_element"]
    
    return elements_by_site

def get_sites_by_alchemical_stage(stage: AlchemicalStage) -> List[SacredSite]:
    """Get sites associated with a specific alchemical stage."""
    matching_sites = []
    
    for site in SACRED_SITES.values():
        if "alchemical_stage" in site.cultural_elements and stage.value in site.cultural_elements["alchemical_stage"]:
            matching_sites.append(site)
    
    return matching_sites

def get_sites_by_hopi_direction(direction: Direction) -> List[SacredSite]:
    """Get sites associated with a specific Hopi direction."""
    matching_sites = []
    
    for site in SACRED_SITES.values():
        if "direction" in site.cultural_elements and direction.value in site.cultural_elements["direction"]:
            matching_sites.append(site)
    
    return matching_sites 