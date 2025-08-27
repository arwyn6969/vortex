"""
Mythology Framework

This package provides tools for working with mythological systems,
their archetypes, and relationships to celestial phenomena across cultures.
"""

# We need to update the import structure to avoid circular imports
# First, let's import the core modules without any circular dependencies
from . import archetype_manager
from . import cross_cultural
from . import celestial_bodies
from . import celestial_alignments

# Cultural mythology modules
from . import (
    mayan, 
    dogon, 
    egyptian, 
    greco_roman, 
    norse,
    hindu, 
    aboriginal,
    celtic, 
    chinese_astronomy, 
    tatar,
    aztec,
    persian,
    yoruba,
    syrian,
    hopi
)

# Now we can safely import modules that might depend on the above
from . import sacred_sites
from . import alignment_analysis
from . import validation  # Import validation for MythologyValidator

# Finally, import any validation modules that depend on everything else
# from . import validator  # Comment this out as it's causing circular imports

# Expose key classes and functions
from .archetype_manager import ArchetypeManager
from .validation import MythologyValidator  # Use MythologyValidator instead of ArchetypeValidator
from .cross_cultural import (
    get_equivalent_deity, 
    find_shared_symbolism, 
    get_celestial_correspondences
)
from .celestial_alignments import (
    CelestialBody, 
    AlignmentType, 
    calculate_position, 
    get_celestial_significance
)
from .sacred_sites import (
    SacredSite, 
    get_site_by_name, 
    get_sites_by_culture,
    get_sites_by_alignment,
    get_sites_with_zenith_passages,
    find_mythological_connections,
    SiteType,
    CultureType,
    # Update with our new functions
    get_syrian_alchemical_sites,
    get_hopi_sites,
    calculate_site_alignments_for_date,
    get_alignment_seasonal_variation
)
from .alignment_analysis import (
    AlignmentPattern,
    CrossCulturalAnalysis,
    MythologicalConnections,
    # Update with our new classes
    SyrianAlchemicalAnalysis,
    HopiSiteAnalysis,
    calculate_alignment_accuracy,
    find_optimal_observation_date
)

# Update the __all__ list
__all__ = [
    # Classes
    'ArchetypeManager',
    'MythologyValidator',  # Changed from 'ArchetypeValidator'
    'CelestialBody',
    'AlignmentType',
    'SacredSite',
    'AlignmentPattern',
    'CrossCulturalAnalysis',
    'MythologicalConnections',
    'SyrianAlchemicalAnalysis',
    'HopiSiteAnalysis',
    'SiteType',
    'CultureType',
    
    # Functions
    'get_equivalent_deity',
    'find_shared_symbolism',
    'get_celestial_correspondences',
    'calculate_position',
    'get_celestial_significance',
    'get_site_by_name',
    'get_sites_by_culture',
    'get_sites_by_alignment',
    'get_sites_with_zenith_passages',
    'find_mythological_connections',
    'get_syrian_alchemical_sites',
    'get_hopi_sites',
    'calculate_site_alignments_for_date',
    'get_alignment_seasonal_variation',
    'calculate_alignment_accuracy',
    'find_optimal_observation_date'
] 