"""
Sacred geometry visualization and calculations for mythological patterns.
"""
from typing import Dict, List, Tuple
import math

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