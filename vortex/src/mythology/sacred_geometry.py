"""
Sacred Geometry Validation and Pattern Generation

This module handles the validation and generation of sacred geometric patterns
across different mythological traditions. It ensures proper proportions,
alignments, and symbolic meanings are maintained.
"""

import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .result import ValidationResult

class GeometryType(Enum):
    """Types of sacred geometric patterns."""
    FLOWER_OF_LIFE = "flower_of_life"
    METATRONS_CUBE = "metatrons_cube"
    SRI_YANTRA = "sri_yantra"
    SEED_OF_LIFE = "seed_of_life"
    TREE_OF_LIFE = "tree_of_life"
    VESICA_PISCIS = "vesica_piscis"
    GOLDEN_SPIRAL = "golden_spiral"
    TORUS = "torus"

@dataclass
class GeometricPattern:
    """Representation of a sacred geometric pattern."""
    type: GeometryType
    points: List[Tuple[float, float]]
    circles: List[Tuple[float, float, float]]  # x, y, radius
    lines: List[Tuple[Tuple[float, float], Tuple[float, float]]]
    proportions: Dict[str, float]
    symbolism: Dict[str, str]

class ProportionValidator:
    """Validates sacred proportions in geometric patterns."""
    
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
    SQRT2 = math.sqrt(2)  # Square root of 2
    SQRT3 = math.sqrt(3)  # Square root of 3
    
    @staticmethod
    def validate_golden_ratio(ratio: float, tolerance: float = 0.001) -> bool:
        """Validate if a ratio matches the golden ratio."""
        return abs(ratio - ProportionValidator.PHI) < tolerance
    
    @staticmethod
    def validate_sqrt2_ratio(ratio: float, tolerance: float = 0.001) -> bool:
        """Validate if a ratio matches sqrt(2)."""
        return abs(ratio - ProportionValidator.SQRT2) < tolerance
    
    @staticmethod
    def validate_sqrt3_ratio(ratio: float, tolerance: float = 0.001) -> bool:
        """Validate if a ratio matches sqrt(3)."""
        return abs(ratio - ProportionValidator.SQRT3) < tolerance
    
    @staticmethod
    def validate_vesica_piscis(pattern: GeometricPattern) -> bool:
        """Validate vesica piscis proportions."""
        if not pattern.circles or len(pattern.circles) < 2:
            return False
            
        c1, c2 = pattern.circles[:2]
        distance = math.sqrt((c2[0] - c1[0])**2 + (c2[1] - c1[1])**2)
        radius = c1[2]  # Both circles should have same radius
        
        return abs(distance - radius) < 0.001

def validate_pattern(pattern_name: str, geometry_data: Dict) -> ValidationResult:
    """Validate a sacred geometric pattern."""
    try:
        pattern_type = GeometryType(pattern_name)
    except ValueError:
        return ValidationResult(
            False,
            [f"Unknown pattern type: {pattern_name}"],
            ["Use one of the known sacred geometry patterns"],
            0.0,
            []
        )
    
    validator = _get_pattern_validator(pattern_type)
    if not validator:
        return ValidationResult(
            False,
            ["Pattern validator not implemented"],
            [],
            0.0,
            []
        )
        
    return validator(geometry_data)

def _get_pattern_validator(pattern_type: GeometryType):
    """Get the appropriate validator function for a pattern type."""
    validators = {
        GeometryType.FLOWER_OF_LIFE: _validate_flower_of_life,
        GeometryType.METATRONS_CUBE: _validate_metatrons_cube,
        GeometryType.SRI_YANTRA: _validate_sri_yantra,
        GeometryType.SEED_OF_LIFE: _validate_seed_of_life,
        GeometryType.TREE_OF_LIFE: _validate_tree_of_life,
        GeometryType.VESICA_PISCIS: _validate_vesica_piscis,
        GeometryType.GOLDEN_SPIRAL: _validate_golden_spiral,
        GeometryType.TORUS: _validate_torus
    }
    return validators.get(pattern_type)

def _validate_flower_of_life(data: Dict) -> ValidationResult:
    """Validate Flower of Life pattern."""
    issues = []
    suggestions = []
    
    # Check number of circles
    if "circles" not in data:
        issues.append("Missing circle count")
        suggestions.append("Flower of Life should specify number of circles")
        return ValidationResult(False, issues, suggestions, 0.0, [])
        
    if data["circles"] not in {7, 19, 37, 61}:
        issues.append("Invalid circle count")
        suggestions.append("Flower of Life should have 7, 19, 37, or 61 circles")
        
    # Check radius ratio
    if "radius_ratio" not in data:
        issues.append("Missing radius ratio")
    elif not ProportionValidator.validate_sqrt3_ratio(data["radius_ratio"]):
        issues.append("Invalid radius ratio")
        suggestions.append("Radius ratio should be √3")
        
    confidence = 1.0 - (len(issues) * 0.2)
    return ValidationResult(
        len(issues) == 0,
        issues,
        suggestions,
        max(0.0, confidence),
        ["Sacred Geometry: The Flower of Life"]
    )

def _validate_metatrons_cube(data: Dict) -> ValidationResult:
    """Validate Metatron's Cube pattern."""
    issues = []
    suggestions = []
    
    required_elements = {
        "center_point": bool,
        "platonic_solids": list,
        "connecting_lines": int
    }
    
    for element, type_ in required_elements.items():
        if element not in data:
            issues.append(f"Missing {element}")
        elif not isinstance(data[element], type_):
            issues.append(f"Invalid {element} type")
            
    if "platonic_solids" in data:
        valid_solids = {"tetrahedron", "cube", "octahedron", "dodecahedron", "icosahedron"}
        for solid in data["platonic_solids"]:
            if solid not in valid_solids:
                issues.append(f"Invalid platonic solid: {solid}")
                
    confidence = 1.0 - (len(issues) * 0.2)
    return ValidationResult(
        len(issues) == 0,
        issues,
        suggestions,
        max(0.0, confidence),
        ["Sacred Geometry: Metatron's Cube"]
    )

def _validate_sri_yantra(data: Dict) -> ValidationResult:
    """Validate Sri Yantra pattern."""
    issues = []
    suggestions = []
    
    # Check triangle count
    if "triangles" not in data:
        issues.append("Missing triangle count")
    elif data["triangles"] != 9:
        issues.append("Sri Yantra must have 9 interlocking triangles")
        
    # Check intersection points
    if "intersection_points" not in data:
        issues.append("Missing intersection points")
    elif data["intersection_points"] != 43:
        issues.append("Sri Yantra must have 43 intersection points")
        
    confidence = 1.0 - (len(issues) * 0.2)
    return ValidationResult(
        len(issues) == 0,
        issues,
        suggestions,
        max(0.0, confidence),
        ["Sacred Geometry: Sri Yantra"]
    )

def _validate_seed_of_life(data: Dict) -> ValidationResult:
    """Validate Seed of Life pattern."""
    issues = []
    suggestions = []
    
    if "circles" not in data:
        issues.append("Missing circle count")
    elif data["circles"] != 7:
        issues.append("Seed of Life must have 7 circles")
        
    confidence = 1.0 - (len(issues) * 0.2)
    return ValidationResult(
        len(issues) == 0,
        issues,
        suggestions,
        max(0.0, confidence),
        ["Sacred Geometry: The Seed of Life"]
    )

def _validate_tree_of_life(data: Dict) -> ValidationResult:
    """Validate Tree of Life pattern."""
    issues = []
    suggestions = []
    
    # Check sephirot count
    if "sephirot" not in data:
        issues.append("Missing sephirot count")
    elif data["sephirot"] != 10:
        issues.append("Tree of Life must have 10 sephirot")
        
    # Check paths
    if "paths" not in data:
        issues.append("Missing paths")
    elif data["paths"] != 22:
        issues.append("Tree of Life must have 22 paths")
        
    confidence = 1.0 - (len(issues) * 0.2)
    return ValidationResult(
        len(issues) == 0,
        issues,
        suggestions,
        max(0.0, confidence),
        ["Sacred Geometry: The Tree of Life"]
    )

def _validate_vesica_piscis(data: Dict) -> ValidationResult:
    """Validate Vesica Piscis pattern."""
    issues = []
    suggestions = []
    
    if "circles" not in data:
        issues.append("Missing circles")
    elif data["circles"] != 2:
        issues.append("Vesica Piscis must have exactly 2 circles")
        
    if "intersection_points" not in data:
        issues.append("Missing intersection points")
    elif data["intersection_points"] != 2:
        issues.append("Vesica Piscis must have 2 intersection points")
        
    confidence = 1.0 - (len(issues) * 0.2)
    return ValidationResult(
        len(issues) == 0,
        issues,
        suggestions,
        max(0.0, confidence),
        ["Sacred Geometry: Vesica Piscis"]
    )

def _validate_golden_spiral(data: Dict) -> ValidationResult:
    """Validate Golden Spiral pattern."""
    issues = []
    suggestions = []
    
    if "growth_factor" not in data:
        issues.append("Missing growth factor")
    elif not ProportionValidator.validate_golden_ratio(data["growth_factor"]):
        issues.append("Growth factor must match the golden ratio")
        
    confidence = 1.0 - (len(issues) * 0.2)
    return ValidationResult(
        len(issues) == 0,
        issues,
        suggestions,
        max(0.0, confidence),
        ["Sacred Geometry: The Golden Spiral"]
    )

def _validate_torus(data: Dict) -> ValidationResult:
    """Validate Torus pattern."""
    issues = []
    suggestions = []
    
    if "major_radius" not in data or "minor_radius" not in data:
        issues.append("Missing radius values")
    elif "ratio" not in data:
        issues.append("Missing radius ratio")
    elif not ProportionValidator.validate_golden_ratio(data["ratio"]):
        issues.append("Radius ratio should match the golden ratio")
        
    confidence = 1.0 - (len(issues) * 0.2)
    return ValidationResult(
        len(issues) == 0,
        issues,
        suggestions,
        max(0.0, confidence),
        ["Sacred Geometry: The Torus"]
    )

def generate_kan_cross() -> List[str]:
    """Generate ASCII art representation of the Kan Cross (four directions)."""
    pattern = [
        "    †    ",
        "    |    ",
        "    |    ",
        "†───┼───†",
        "    |    ",
        "    |    ",
        "    †    "
    ]
    return pattern

def generate_quincunx() -> List[str]:
    """Generate ASCII art representation of the Quincunx (five-point pattern)."""
    pattern = [
        "  †   †  ",
        "    ∙    ",
        "†  ◊  †",
        "    ∙    ",
        "  †   †  "
    ]
    return pattern

def generate_hexagon() -> List[str]:
    """Generate ASCII art representation of the Hexagon."""
    pattern = [
        "   ____   ",
        " /      \\ ",
        "/    ◊    \\",
        "\\         /",
        " \\______/ "
    ]
    return pattern

def generate_octagon() -> List[str]:
    """Generate ASCII art representation of the Octagon."""
    pattern = [
        "  ____  ",
        " /    \\ ",
        "/      \\",
        "|   ◊  |",
        "\\      /",
        " \\____/ "
    ]
    return pattern

def calculate_temple_alignment(pattern_name: str, latitude: float, solstice_date: bool = False) -> Dict[str, float]:
    """Calculate optimal temple alignment angles based on sacred geometry pattern.
    
    Args:
        pattern_name: Name of the sacred geometry pattern
        latitude: Location latitude in degrees
        solstice_date: Whether to align for solstice (True) or equinox (False)
    
    Returns:
        Dictionary containing alignment angles and ratios
    """
    # Base angle calculations
    equinox_angle = 90.0  # East-West alignment
    solstice_angle = 23.5  # Earth's axial tilt
    
    # Pattern-specific adjustments
    if pattern_name == "kan_cross":
        cardinal_angles = [0, 90, 180, 270]  # NSEW
        main_angle = equinox_angle
    elif pattern_name == "quincunx":
        cardinal_angles = [0, 72, 144, 216, 288]  # Five-fold symmetry
        main_angle = equinox_angle + (solstice_angle if solstice_date else 0)
    elif pattern_name == "hexagon":
        cardinal_angles = [i * 60 for i in range(6)]  # Six-fold symmetry
        main_angle = equinox_angle + (solstice_angle/2 if solstice_date else 0)
    elif pattern_name == "octagon":
        cardinal_angles = [i * 45 for i in range(8)]  # Eight-fold symmetry
        main_angle = equinox_angle + (solstice_angle/3 if solstice_date else 0)
    else:
        raise ValueError(f"Unknown pattern: {pattern_name}")
    
    # Adjust for latitude
    adjusted_angles = [
        angle + (math.sin(math.radians(latitude)) * solstice_angle)
        for angle in cardinal_angles
    ]
    
    return {
        "main_angle": main_angle,
        "cardinal_angles": adjusted_angles,
        "latitude_adjustment": math.sin(math.radians(latitude)) * solstice_angle,
        "golden_ratio": (1 + math.sqrt(5)) / 2,  # Sacred proportion
        "pattern_points": len(cardinal_angles)
    }

def calculate_observatory_points(pattern_name: str, center: Tuple[float, float], radius: float) -> List[Tuple[float, float]]:
    """Calculate observation points for astronomical alignments.
    
    Args:
        pattern_name: Name of the sacred geometry pattern
        center: (x, y) coordinates of the center point
        radius: Radius of the observation circle
    
    Returns:
        List of (x, y) coordinates for observation points
    """
    points = []
    cx, cy = center
    
    if pattern_name == "kan_cross":
        angles = [0, 90, 180, 270]  # Four cardinal directions
    elif pattern_name == "quincunx":
        angles = [0, 72, 144, 216, 288]  # Five points
    elif pattern_name == "hexagon":
        angles = [i * 60 for i in range(6)]  # Six points
    elif pattern_name == "octagon":
        angles = [i * 45 for i in range(8)]  # Eight points
    else:
        raise ValueError(f"Unknown pattern: {pattern_name}")
    
    # Calculate points on circle
    for angle in angles:
        rad = math.radians(angle)
        x = cx + radius * math.cos(rad)
        y = cy + radius * math.sin(rad)
        points.append((x, y))
    
    return points

def get_pattern_visualization(pattern_name: str) -> List[str]:
    """Get ASCII art visualization of a sacred geometry pattern."""
    patterns = {
        "kan_cross": generate_kan_cross,
        "quincunx": generate_quincunx,
        "hexagon": generate_hexagon,
        "octagon": generate_octagon
    }
    
    if pattern_name not in patterns:
        raise ValueError(f"Unknown pattern: {pattern_name}")
    
    return patterns[pattern_name]()

def calculate_sacred_proportions(pattern_name: str) -> Dict[str, float]:
    """Calculate sacred proportions for a geometric pattern."""
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    
    proportions = {
        "kan_cross": {
            "width_to_height": 1.0,  # Perfect square
            "center_to_arm": 1/phi,
            "arm_length_ratio": 1/3
        },
        "quincunx": {
            "width_to_height": phi,  # Golden rectangle
            "point_spacing": 1/phi,
            "center_to_corner": 1.0
        },
        "hexagon": {
            "width_to_height": math.sqrt(3)/2,
            "inner_to_outer": 1/2,
            "point_spacing": 1/3
        },
        "octagon": {
            "width_to_height": 1.0,
            "inner_to_outer": 1/math.sqrt(2),
            "point_spacing": 1/4
        }
    }
    
    if pattern_name not in proportions:
        raise ValueError(f"Unknown pattern: {pattern_name}")
    
    return proportions[pattern_name] 