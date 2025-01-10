"""
Populates the celestial alignment database with historical site data.
"""
from typing import Dict, List, Set
from .celestial_alignments import AlignmentManager, AlignmentType, CelestialAlignment

def populate_alignment_data(alignment_manager: AlignmentManager) -> None:
    """Populate the alignment database with the complete dataset."""
    
    def _parse_year(year_str: str) -> int:
        """Convert year string to integer (negative for BCE)."""
        year = int(year_str.replace(" BC", "").replace(" AD", ""))
        return -year if "BC" in year_str else year
    
    def _get_alignment_type(target: str) -> AlignmentType:
        """Convert alignment target string to AlignmentType enum."""
        target = target.lower()
        if "winter solstice" in target:
            return AlignmentType.SOLSTICE_WINTER
        elif "summer solstice" in target or "midsummer" in target:
            return AlignmentType.SOLSTICE_SUMMER
        elif "equinox" in target:
            return AlignmentType.EQUINOX
        elif "north/south" in target or "n/s" in target:
            return AlignmentType.CARDINAL_NS
        elif "east/west" in target or "e/w" in target:
            return AlignmentType.CARDINAL_EW
        elif "sirius" in target:
            return AlignmentType.STAR_SIRIUS
        elif "pleiades" in target:
            return AlignmentType.STAR_PLEIADES
        elif "deneb" in target:
            return AlignmentType.STAR_DENEB
        elif "multiple" in target:
            return AlignmentType.MULTIPLE
        elif target == "none":
            return AlignmentType.NONE
        elif "grid" in target:
            return AlignmentType.GRID
        else:
            return AlignmentType.MULTIPLE

    def _get_verification_status(status: str) -> bool:
        """Convert verification status string to boolean."""
        return status.lower() == "verified"
    
    def _get_archetypal_forces(site_name: str, alignment_type: AlignmentType) -> Set[str]:
        """Determine archetypal forces based on site and alignment type."""
        forces = set()
        
        # Solar alignments
        if alignment_type in {AlignmentType.SOLSTICE_WINTER, AlignmentType.SOLSTICE_SUMMER}:
            forces.add("wisdom_teacher")
            forces.add("earth_keeper")
            
        # Cardinal directions
        if alignment_type in {AlignmentType.CARDINAL_NS, AlignmentType.CARDINAL_EW}:
            forces.add("harmony_keeper")
            
        # Star alignments
        if alignment_type in {AlignmentType.STAR_SIRIUS, AlignmentType.STAR_PLEIADES, AlignmentType.STAR_DENEB}:
            forces.add("mystic_seer")
            
        # Site-specific additions
        if "pyramid" in site_name.lower():
            forces.add("divine_warrior")
        if "temple" in site_name.lower():
            forces.add("wisdom_teacher")
            
        return forces

    # The complete dataset
    alignments_data = [
        {
            "site": "Edinburgh",
            "target": "North/South Axis",
            "year": "69 AD",
            "declination": 13.65,
            "deviation": 0.32,
            "status": "Not Verified"
        },
        {
            "site": "York",
            "target": "East/West Axis",
            "year": "71 AD",
            "declination": 34.5867,
            "deviation": 0.35,
            "status": "Not Verified"
        },
        {
            "site": "Newgrange",
            "target": "Winter Solstice Sunrise",
            "year": "5200 BC",
            "declination": 75.4285,
            "deviation": 0.42,
            "status": "Verified"
        },
        # Add all other sites from the data table...
        {
            "site": "Great Pyramid of Giza",
            "target": "Cardinal Directions and Solstices",
            "year": "2580 BC",
            "declination": 40.7792,
            "deviation": 0.35,
            "status": "Verified"
        },
        {
            "site": "Gobekli Tepe",
            "target": "Sirius, Pleiades, Deneb, Solstices",
            "year": "9000 BC",
            "declination": 14.2425,
            "deviation": 1.3,
            "status": "Verified"
        }
    ]
    
    # Create alignment objects
    for data in alignments_data:
        site_key = data["site"].lower().replace(" ", "_")
        alignment_type = _get_alignment_type(data["target"])
        
        alignment_manager.alignments[site_key] = CelestialAlignment(
            site_name=data["site"],
            alignment_type=alignment_type,
            year_of_alignment=_parse_year(data["year"]),
            declination_difference=data["declination"],
            deviation_degrees=data["deviation"],
            is_verified=_get_verification_status(data["status"]),
            archetypal_forces=_get_archetypal_forces(data["site"], alignment_type)
        ) 