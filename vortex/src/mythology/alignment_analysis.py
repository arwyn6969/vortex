"""
Sacred Site Alignment Analysis

This module provides tools for analyzing and comparing celestial alignments
across different sacred sites and cultural traditions. It helps identify
patterns, similarities, and differences in how various cultures integrated
astronomical knowledge into their sacred architecture.
"""

from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import math

from .sacred_sites import (
    SacredSite, CelestialAlignment, SACRED_SITES, get_site_by_name,
    get_sites_by_culture, get_syrian_alchemical_sites, get_hopi_sites,
    CultureType, SiteType, AlignmentMathModel
)
from .celestial_alignments import CelestialBody, AlignmentType
from .cross_cultural import get_celestial_correspondences, get_elemental_correspondences
from .syrian import AlchemicalStage, AlchemicalElement
from .hopi import Direction, WorldCycle

class AlignmentPattern:
    """Identifies and analyzes patterns in sacred site alignments."""
    
    @staticmethod
    def find_common_alignments(sites: List[SacredSite]) -> Dict[str, List[SacredSite]]:
        """Find common alignment patterns across multiple sites."""
        alignment_patterns = {}
        
        for site in sites:
            for alignment in site.alignments:
                key = f"{alignment.alignment_type.value}_{alignment.primary_body.value}"
                if key not in alignment_patterns:
                    alignment_patterns[key] = []
                alignment_patterns[key].append(site)
        
        # Filter to patterns that appear in multiple sites
        return {k: v for k, v in alignment_patterns.items() if len(v) > 1}
    
    @staticmethod
    def find_axis_mundi_sites() -> List[SacredSite]:
        """Find sites that represent the 'axis mundi' or cosmic axis concept."""
        axis_mundi_sites = []
        
        for site_key, site in SACRED_SITES.items():
            # Sites with zenith passages often embody the axis mundi concept
            if site.zenith_passages:
                axis_mundi_sites.append(site)
                continue
                
            # Sites with specific alignments to polar or central stars
            for alignment in site.alignments:
                if alignment.primary_body in [
                    CelestialBody.POLARIS, 
                    CelestialBody.DRACO
                ]:
                    axis_mundi_sites.append(site)
                    break
        
        return axis_mundi_sites
    
    @staticmethod
    def find_solstice_sites() -> Dict[str, List[SacredSite]]:
        """Find sites with significant solstice alignments."""
        solstice_sites = {
            "summer": [],
            "winter": []
        }
        
        for site_key, site in SACRED_SITES.items():
            for alignment in site.alignments:
                if alignment.alignment_type == AlignmentType.SOLSTICE_SUMMER:
                    solstice_sites["summer"].append(site)
                elif alignment.alignment_type == AlignmentType.SOLSTICE_WINTER:
                    solstice_sites["winter"].append(site)
        
        return solstice_sites
    
    @staticmethod
    def find_equinox_sites() -> List[SacredSite]:
        """Find sites with significant equinox alignments."""
        equinox_sites = []
        
        for site_key, site in SACRED_SITES.items():
            for alignment in site.alignments:
                if alignment.alignment_type in [
                    AlignmentType.EQUINOX_SPRING,
                    AlignmentType.EQUINOX_AUTUMN
                ]:
                    equinox_sites.append(site)
                    break
        
        return equinox_sites
    
    @staticmethod
    def find_sites_with_math_models() -> Dict[str, List[str]]:
        """Find sites that have mathematical alignment models by culture."""
        sites_with_models = {}
        
        for site_key, site in SACRED_SITES.items():
            has_model = False
            for alignment in site.alignments:
                if alignment.math_model:
                    has_model = True
                    break
                    
            if has_model:
                culture = site.culture.value
                if culture not in sites_with_models:
                    sites_with_models[culture] = []
                sites_with_models[culture].append(site.name)
        
        return sites_with_models
    
    @staticmethod
    def find_sites_with_seasonal_variations() -> Dict[str, Dict[str, List[str]]]:
        """Find sites that document seasonal variations in their alignments."""
        seasonal_sites = {}
        
        for site_key, site in SACRED_SITES.items():
            season_details = {}
            for alignment in site.alignments:
                if alignment.seasonal_variations:
                    for season, description in alignment.seasonal_variations.items():
                        if season not in season_details:
                            season_details[season] = []
                        season_details[season].append(
                            f"{alignment.alignment_type.value}_{alignment.primary_body.value}: {description}"
                        )
            
            if season_details:
                seasonal_sites[site.name] = season_details
        
        return seasonal_sites

class CrossCulturalAnalysis:
    """Analyzes alignments across different cultural traditions."""
    
    @staticmethod
    def compare_sites(site1_name: str, site2_name: str) -> Dict:
        """Compare astronomical alignments between two sacred sites."""
        site1 = get_site_by_name(site1_name)
        site2 = get_site_by_name(site2_name)
        
        if not site1 or not site2:
            return {"error": "One or both sites not found"}
        
        comparison = {
            "site1": site1.name,
            "site2": site2.name,
            "culture1": site1.culture.value,
            "culture2": site2.culture.value,
            "time_difference": abs(site1.date_range[0] - site2.date_range[0]),
            "shared_alignments": [],
            "shared_mythological_themes": [],
            "unique_alignments": {
                site1.name: [],
                site2.name: []
            }
        }
        
        # Find shared alignments
        alignment_types1 = [(a.alignment_type, a.primary_body) for a in site1.alignments]
        alignment_types2 = [(a.alignment_type, a.primary_body) for a in site2.alignments]
        
        for alignment_pair in alignment_types1:
            if alignment_pair in alignment_types2:
                comparison["shared_alignments"].append({
                    "type": alignment_pair[0].value,
                    "body": alignment_pair[1].value
                })
            else:
                comparison["unique_alignments"][site1.name].append({
                    "type": alignment_pair[0].value,
                    "body": alignment_pair[1].value
                })
                
        for alignment_pair in alignment_types2:
            if alignment_pair not in alignment_types1:
                comparison["unique_alignments"][site2.name].append({
                    "type": alignment_pair[0].value,
                    "body": alignment_pair[1].value
                })
        
        # Find shared mythological themes
        shared_mythologies = set(site1.mythological_connections.keys()) & set(site2.mythological_connections.keys())
        
        for mythology in shared_mythologies:
            comparison["shared_mythological_themes"].append({
                "mythology": mythology,
                site1.name: site1.mythological_connections[mythology],
                site2.name: site2.mythological_connections[mythology]
            })
        
        # Add analysis of mathematical models if both sites have them
        comparison["mathematical_models"] = {
            site1.name: has_math_models(site1),
            site2.name: has_math_models(site2)
        }
        
        # Add analysis of cultural elements if both sites have them
        if site1.cultural_elements and site2.cultural_elements:
            comparison["cultural_elements"] = {
                "shared": {},
                "unique": {
                    site1.name: {},
                    site2.name: {}
                }
            }
            
            for element_type in set(site1.cultural_elements.keys()) & set(site2.cultural_elements.keys()):
                shared_elements = set(site1.cultural_elements[element_type]) & set(site2.cultural_elements[element_type])
                if shared_elements:
                    comparison["cultural_elements"]["shared"][element_type] = list(shared_elements)
            
            for element_type in site1.cultural_elements:
                if element_type not in site2.cultural_elements:
                    comparison["cultural_elements"]["unique"][site1.name][element_type] = site1.cultural_elements[element_type]
                else:
                    unique_elements = set(site1.cultural_elements[element_type]) - set(site2.cultural_elements[element_type])
                    if unique_elements:
                        comparison["cultural_elements"]["unique"][site1.name][element_type] = list(unique_elements)
            
            for element_type in site2.cultural_elements:
                if element_type not in site1.cultural_elements:
                    comparison["cultural_elements"]["unique"][site2.name][element_type] = site2.cultural_elements[element_type]
                else:
                    unique_elements = set(site2.cultural_elements[element_type]) - set(site1.cultural_elements[element_type])
                    if unique_elements:
                        comparison["cultural_elements"]["unique"][site2.name][element_type] = list(unique_elements)
        
        return comparison
    
    @staticmethod
    def find_celestial_body_significance(body: CelestialBody) -> Dict[str, Dict]:
        """Compare significance of a celestial body across different traditions."""
        return get_celestial_correspondences(body.value)
    
    @staticmethod
    def analyze_zenith_sites() -> Dict:
        """Analyze sites with zenith passages and their cultural significance."""
        zenith_sites = [site for site in SACRED_SITES.values() if site.zenith_passages]
        
        analysis = {
            "count": len(zenith_sites),
            "sites": [site.name for site in zenith_sites],
            "latitude_range": (
                min([site.location[0] for site in zenith_sites]) if zenith_sites else None,
                max([site.location[0] for site in zenith_sites]) if zenith_sites else None
            ),
            "cultural_distribution": {},
            "primary_bodies": {}
        }
        
        for site in zenith_sites:
            # Count cultures
            if site.culture.value not in analysis["cultural_distribution"]:
                analysis["cultural_distribution"][site.culture.value] = 0
            analysis["cultural_distribution"][site.culture.value] += 1
            
            # Count celestial bodies
            for body in site.zenith_passages:
                if body.value not in analysis["primary_bodies"]:
                    analysis["primary_bodies"][body.value] = 0
                analysis["primary_bodies"][body.value] += 1
        
        return analysis
    
    @staticmethod
    def compare_mathematical_models(site1_name: str, site2_name: str, date: datetime) -> Dict:
        """Compare the mathematical alignment models of two sites for a specific date."""
        site1 = get_site_by_name(site1_name)
        site2 = get_site_by_name(site2_name)
        
        if not site1 or not site2:
            return {"error": "One or both sites not found"}
        
        site1_alignments = site1.calculate_alignments_for_date(date)
        site2_alignments = site2.calculate_alignments_for_date(date)
        
        # Compare common alignment types
        common_alignments = {}
        for key in set(site1_alignments.keys()) & set(site2_alignments.keys()):
            common_alignments[key] = {
                site1.name: site1_alignments[key],
                site2.name: site2_alignments[key],
                "azimuth_difference": abs(site1_alignments[key].get("azimuth", 0) - 
                                         site2_alignments[key].get("azimuth", 0)),
                "altitude_difference": abs(site1_alignments[key].get("altitude", 0) - 
                                          site2_alignments[key].get("altitude", 0)),
                "strength_difference": abs(site1_alignments[key].get("alignment_strength", 0) - 
                                          site2_alignments[key].get("alignment_strength", 0))
            }
        
        return {
            "date": date.isoformat(),
            "site1": site1.name,
            "site2": site2.name,
            "common_alignments": common_alignments,
            "unique_to_site1": list(set(site1_alignments.keys()) - set(site2_alignments.keys())),
            "unique_to_site2": list(set(site2_alignments.keys()) - set(site1_alignments.keys()))
        }

class MythologicalConnections:
    """Analyzes mythological connections between celestial alignments and sacred sites."""
    
    @staticmethod
    def get_solar_deity_sites() -> Dict[str, List[str]]:
        """Find sacred sites associated with solar deities across cultures."""
        solar_sites = {}
        
        for site_key, site in SACRED_SITES.items():
            has_solar_alignment = False
            
            # Check for solar alignments
            for alignment in site.alignments:
                if alignment.primary_body == CelestialBody.SUN:
                    has_solar_alignment = True
                    break
            
            if has_solar_alignment:
                for mythology, connection in site.mythological_connections.items():
                    # Look for solar deity references
                    if any(term in connection.lower() for term in [
                        "sun", "solar", "ra", "apollo", "helios", "kinich", "taiowa"
                    ]):
                        if mythology not in solar_sites:
                            solar_sites[mythology] = []
                        solar_sites[mythology].append(site.name)
        
        return solar_sites
    
    @staticmethod
    def get_creation_sites() -> List[SacredSite]:
        """Find sites associated with creation myths."""
        creation_sites = []
        
        for site_key, site in SACRED_SITES.items():
            for mythology, connection in site.mythological_connections.items():
                if any(term in connection.lower() for term in [
                    "creation", "born", "emerge", "origin", "beginning", "genesis"
                ]):
                    creation_sites.append(site)
                    break
        
        return creation_sites
    
    @staticmethod
    def get_afterlife_sites() -> List[SacredSite]:
        """Find sites associated with afterlife or underworld concepts."""
        afterlife_sites = []
        
        for site_key, site in SACRED_SITES.items():
            for mythology, connection in site.mythological_connections.items():
                if any(term in connection.lower() for term in [
                    "afterlife", "underworld", "death", "tomb", "burial", "spirit", "ancestor"
                ]):
                    afterlife_sites.append(site)
                    break
        
        return afterlife_sites

class SyrianAlchemicalAnalysis:
    """Specialized analysis of Syrian alchemical sites and their astronomical alignments."""
    
    @staticmethod
    def analyze_alchemical_stages() -> Dict:
        """Analyze how different alchemical stages are represented in site alignments."""
        alchemical_sites = get_syrian_alchemical_sites()
        
        analysis = {
            "count": len(alchemical_sites),
            "sites": [site.name for site in alchemical_sites],
            "stages": {},
            "elements": {},
            "celestial_bodies": {}
        }
        
        for site in alchemical_sites:
            # Analyze alchemical stages in cultural elements
            if "alchemical_stage" in site.cultural_elements:
                for stage in site.cultural_elements["alchemical_stage"]:
                    if stage not in analysis["stages"]:
                        analysis["stages"][stage] = []
                    analysis["stages"][stage].append(site.name)
            
            # Analyze alchemical elements in cultural elements
            if "alchemical_element" in site.cultural_elements:
                for element in site.cultural_elements["alchemical_element"]:
                    if element not in analysis["elements"]:
                        analysis["elements"][element] = []
                    analysis["elements"][element].append(site.name)
            
            # Analyze celestial bodies in alignments
            for alignment in site.alignments:
                body = alignment.primary_body.value
                if body not in analysis["celestial_bodies"]:
                    analysis["celestial_bodies"][body] = []
                analysis["celestial_bodies"][body].append(site.name)
        
        return analysis
    
    @staticmethod
    def analyze_alchemical_operations(date: datetime) -> Dict:
        """Analyze optimal times for alchemical operations based on celestial alignments."""
        alchemical_sites = get_syrian_alchemical_sites()
        
        operation_analysis = {
            "date": date.isoformat(),
            "calcination": {"optimal_sites": [], "strength": 0.0},
            "dissolution": {"optimal_sites": [], "strength": 0.0},
            "sublimation": {"optimal_sites": [], "strength": 0.0},
            "coagulation": {"optimal_sites": [], "strength": 0.0}
        }
        
        # Map operations to specific alignment conditions
        operation_conditions = {
            "calcination": {
                "bodies": [CelestialBody.SUN],
                "season_preference": "summer" if 3 <= date.month <= 8 else "winter",
                "preferred_altitude": 60.0  # High in sky
            },
            "dissolution": {
                "bodies": [CelestialBody.MOON],
                "season_preference": "winter" if 3 <= date.month <= 8 else "summer",
                "preferred_altitude": 30.0  # Lower in sky
            },
            "sublimation": {
                "bodies": [CelestialBody.MERCURY],
                "season_preference": "spring" if date.month in [3, 4, 5] else "fall" if date.month in [9, 10, 11] else "neutral",
                "preferred_altitude": 20.0  # Near horizon
            },
            "coagulation": {
                "bodies": [CelestialBody.SATURN],
                "season_preference": "fall" if date.month in [9, 10, 11] else "neutral",
                "preferred_altitude": 45.0  # Middle of sky
            }
        }
        
        for site in alchemical_sites:
            alignments_data = site.calculate_alignments_for_date(date)
            
            for operation, conditions in operation_conditions.items():
                operation_strength = 0.0
                
                # Check alignments for each preferred body
                for body in conditions["bodies"]:
                    key = f"{AlignmentType.RISING.value}_{body.value}"
                    if key in alignments_data:
                        alignment_data = alignments_data[key]
                        
                        # Base strength from alignment calculation
                        base_strength = alignment_data.get("alignment_strength", 0.0)
                        
                        # Adjust for altitude preference
                        altitude = alignment_data.get("altitude", 0.0)
                        altitude_factor = 1.0 - min(1.0, abs(altitude - conditions["preferred_altitude"]) / 60.0)
                        
                        # Adjust for seasonal preference
                        season_factor = 1.0
                        if conditions["season_preference"] != "neutral":
                            if conditions["season_preference"] == "summer" and 3 <= date.month <= 8:
                                season_factor = 1.2
                            elif conditions["season_preference"] == "winter" and (date.month <= 2 or date.month >= 9):
                                season_factor = 1.2
                            elif conditions["season_preference"] == "spring" and date.month in [3, 4, 5]:
                                season_factor = 1.2
                            elif conditions["season_preference"] == "fall" and date.month in [9, 10, 11]:
                                season_factor = 1.2
                            else:
                                season_factor = 0.8
                        
                        # Calculate final strength
                        final_strength = base_strength * altitude_factor * season_factor
                        
                        # Update operation strength with the highest value found
                        operation_strength = max(operation_strength, final_strength)
                
                # Add site to operation analysis if strength is significant
                if operation_strength > 0.5:
                    operation_analysis[operation]["optimal_sites"].append({
                        "site": site.name,
                        "strength": operation_strength
                    })
                    
                    # Update overall operation strength (average)
                    current_sites = len(operation_analysis[operation]["optimal_sites"])
                    current_strength = operation_analysis[operation]["strength"]
                    operation_analysis[operation]["strength"] = (
                        (current_strength * (current_sites - 1) + operation_strength) / current_sites
                        if current_sites > 0 else operation_strength
                    )
        
        return operation_analysis
    
    @staticmethod
    def find_optimal_alchemical_dates(year: int, operation: str) -> List[Dict]:
        """Find optimal dates for specific alchemical operations in a given year."""
        # Map operations to their optimal celestial conditions
        operation_conditions = {
            "calcination": {
                "alignment_type": AlignmentType.SOLSTICE_SUMMER,
                "primary_body": CelestialBody.SUN
            },
            "dissolution": {
                "alignment_type": AlignmentType.CONJUNCTION,
                "primary_body": CelestialBody.MOON
            },
            "sublimation": {
                "alignment_type": AlignmentType.RISING,
                "primary_body": CelestialBody.MERCURY
            },
            "coagulation": {
                "alignment_type": AlignmentType.STATION_DIRECT,
                "primary_body": CelestialBody.SATURN
            }
        }
        
        if operation not in operation_conditions:
            return [{"error": f"Unknown operation: {operation}"}]
        
        conditions = operation_conditions[operation]
        optimal_dates = []
        
        # For demonstration purposes, return simulated optimal dates
        # In a real system, this would use astronomical calculations
        if operation == "calcination":
            # Best near summer solstice
            optimal_dates.append({
                "date": f"{year}-06-21",
                "description": "Summer solstice - maximum solar energy",
                "strength": 1.0
            })
            optimal_dates.append({
                "date": f"{year}-06-22",
                "description": "Day after summer solstice - high solar energy",
                "strength": 0.98
            })
            for i in range(5):
                optimal_dates.append({
                    "date": f"{year}-06-{23+i}",
                    "description": f"Near summer solstice - strong solar energy",
                    "strength": 0.95 - (i * 0.05)
                })
        
        elif operation == "dissolution":
            # Best at full moons
            for month, day in [(1, 10), (2, 9), (3, 10), (4, 8), (5, 7), (6, 5), 
                              (7, 4), (8, 3), (9, 2), (10, 1), (11, 30), (12, 29)]:
                optimal_dates.append({
                    "date": f"{year}-{month:02d}-{day:02d}",
                    "description": f"Full moon in {month:02d}/{year}",
                    "strength": 0.9 + (0.01 * month)  # Slightly stronger in winter
                })
        
        elif operation == "sublimation":
            # Best at Mercury's maximum elongation
            for month, day in [(3, 24), (7, 12), (11, 3)]:
                optimal_dates.append({
                    "date": f"{year}-{month:02d}-{day:02d}",
                    "description": f"Mercury's maximum eastern elongation",
                    "strength": 0.85 + (0.05 * (month % 4))
                })
        
        elif operation == "coagulation":
            # Best when Saturn stations direct
            optimal_dates.append({
                "date": f"{year}-10-11",
                "description": "Saturn stationary direct",
                "strength": 0.95
            })
            for i in range(5):
                optimal_dates.append({
                    "date": f"{year}-10-{12+i}",
                    "description": "Days after Saturn stations direct",
                    "strength": 0.90 - (i * 0.03)
                })
        
        return optimal_dates

class HopiSiteAnalysis:
    """Specialized analysis of Hopi sites and their astronomical alignments."""
    
    @staticmethod
    def analyze_directional_symbolism() -> Dict:
        """Analyze how cardinal directions are represented in Hopi site alignments."""
        hopi_sites = get_hopi_sites()
        
        analysis = {
            "count": len(hopi_sites),
            "sites": [site.name for site in hopi_sites],
            "directions": {},
            "world_cycles": {},
            "ceremonies": {}
        }
        
        direction_alignments = {
            Direction.EAST.value: AlignmentType.RISING,
            Direction.WEST.value: AlignmentType.SETTING,
            Direction.ABOVE.value: AlignmentType.ZENITH,
            Direction.BELOW.value: AlignmentType.NADIR
        }
        
        for site in hopi_sites:
            # Analyze directions in cultural elements
            if "direction" in site.cultural_elements:
                for direction in site.cultural_elements["direction"]:
                    if direction not in analysis["directions"]:
                        analysis["directions"][direction] = []
                    analysis["directions"][direction].append(site.name)
            
            # Analyze world cycles in cultural elements
            if "world_cycle" in site.cultural_elements:
                for cycle in site.cultural_elements["world_cycle"]:
                    if cycle not in analysis["world_cycles"]:
                        analysis["world_cycles"][cycle] = []
                    analysis["world_cycles"][cycle].append(site.name)
            
            # Analyze alignments related to ceremonies
            for alignment in site.alignments:
                if "ceremony" in alignment.cultural_significance.lower():
                    ceremony = alignment.cultural_significance.split("of ")[1].split(" ")[0] if "of " in alignment.cultural_significance else "unknown"
                    if ceremony not in analysis["ceremonies"]:
                        analysis["ceremonies"][ceremony] = []
                    analysis["ceremonies"][ceremony].append(site.name)
        
        return analysis
    
    @staticmethod
    def analyze_kiva_alignments(date: datetime) -> Dict:
        """Analyze kiva alignments and their ceremonial significance on a specific date."""
        hopi_sites = [site for site in get_hopi_sites() if site.site_type == SiteType.KIVA]
        
        kiva_analysis = {
            "date": date.isoformat(),
            "month": date.month,
            "day": date.day,
            "active_ceremonies": [],
            "kiva_alignments": {}
        }
        
        # Map dates to ceremonial periods
        ceremony_periods = {
            (12, 20, 1, 5): "soyal",  # Dec 20 - Jan 5
            (2, 1, 2, 15): "powamu",   # Feb 1 - Feb 15
            (7, 15, 8, 15): "snake_antelope",  # Jul 15 - Aug 15
            (6, 20, 7, 5): "niman"     # Jun 20 - Jul 5
        }
        
        # Check which ceremonial period the date falls into
        current_ceremonies = []
        for (start_month, start_day, end_month, end_day), ceremony in ceremony_periods.items():
            if (date.month > start_month or (date.month == start_month and date.day >= start_day)) and \
               (date.month < end_month or (date.month == end_month and date.day <= end_day)):
                current_ceremonies.append(ceremony)
        
        kiva_analysis["active_ceremonies"] = current_ceremonies
        
        # Analyze alignments for each kiva
        for site in hopi_sites:
            alignments_data = site.calculate_alignments_for_date(date)
            
            site_analysis = {
                "alignments": alignments_data,
                "ceremonial_relevance": {},
                "optimal_time": None
            }
            
            # Determine ceremonial relevance of current alignments
            for ceremony in current_ceremonies:
                if ceremony == "soyal" and any("winter_solstice" in key for key in alignments_data.keys()):
                    site_analysis["ceremonial_relevance"][ceremony] = "high"
                elif ceremony == "niman" and any("summer_solstice" in key for key in alignments_data.keys()):
                    site_analysis["ceremonial_relevance"][ceremony] = "high"
                elif ceremony == "snake_antelope" and any("zenith" in key for key in alignments_data.keys()):
                    site_analysis["ceremonial_relevance"][ceremony] = "high"
                elif ceremony == "powamu" and any("pleiades" in key.lower() for key in alignments_data.keys()):
                    site_analysis["ceremonial_relevance"][ceremony] = "high"
                else:
                    site_analysis["ceremonial_relevance"][ceremony] = "low"
            
            # Find optimal time for observation
            optimal_times = []
            for alignment_key, alignment_data in alignments_data.items():
                if "optimal_time" in alignment_data:
                    optimal_times.append(alignment_data["optimal_time"])
            
            if optimal_times:
                site_analysis["optimal_time"] = optimal_times[0]  # Just use the first one for simplicity
            
            kiva_analysis["kiva_alignments"][site.name] = site_analysis
        
        return kiva_analysis
    
    @staticmethod
    def analyze_world_cycles_representation() -> Dict:
        """Analyze how Hopi world cycles are represented in site alignments."""
        hopi_sites = get_hopi_sites()
        
        analysis = {
            "world_cycles": {},
            "sites_by_cycle": {},
            "element_associations": {}
        }
        
        # Initialize world cycles
        for cycle in WorldCycle:
            analysis["world_cycles"][cycle.value] = {
                "count": 0,
                "sites": []
            }
            analysis["sites_by_cycle"][cycle.value] = []
        
        # Analyze sites
        for site in hopi_sites:
            if "world_cycle" in site.cultural_elements:
                for cycle in site.cultural_elements["world_cycle"]:
                    analysis["world_cycles"][cycle]["count"] += 1
                    analysis["world_cycles"][cycle]["sites"].append(site.name)
                    analysis["sites_by_cycle"][cycle].append(site.name)
                    
                    # Look for elemental associations
                    if "elements" in site.cultural_elements:
                        for element in site.cultural_elements["elements"]:
                            if element not in analysis["element_associations"]:
                                analysis["element_associations"][element] = {}
                            
                            if cycle not in analysis["element_associations"][element]:
                                analysis["element_associations"][element][cycle] = 0
                            analysis["element_associations"][element][cycle] += 1
        
        return analysis

def has_math_models(site: SacredSite) -> bool:
    """Check if a site has mathematical models for its alignments."""
    for alignment in site.alignments:
        if alignment.math_model:
            return True
    return False

def calculate_alignment_accuracy(site: SacredSite, date: datetime) -> Dict[str, float]:
    """Calculate the accuracy of a site's alignments for a specific date."""
    alignment_results = site.calculate_alignments_for_date(date)
    
    # Calculate average alignment strength
    strengths = []
    for alignment_key, data in alignment_results.items():
        if "alignment_strength" in data:
            strengths.append(data["alignment_strength"])
    
    avg_strength = sum(strengths) / len(strengths) if strengths else 0.0
    
    return {
        "site": site.name,
        "date": date.isoformat(),
        "average_strength": avg_strength,
        "alignment_count": len(strengths),
        "alignments": alignment_results
    }

def find_optimal_observation_date(site_name: str, alignment_type: AlignmentType, 
                                 body: CelestialBody, year: int) -> Dict:
    """Find the optimal date to observe a specific alignment at a site in a given year."""
    site = get_site_by_name(site_name)
    if not site:
        return {"error": "Site not found"}
    
    # Find the matching alignment
    target_alignment = None
    for alignment in site.alignments:
        if alignment.alignment_type == alignment_type and alignment.primary_body == body:
            target_alignment = alignment
            break
    
    if not target_alignment:
        return {"error": "Alignment not found at this site"}
    
    if not target_alignment.math_model:
        return {"error": "No mathematical model available for this alignment"}
    
    # For demonstration purposes, return simulated optimal dates
    # In a real system, this would perform astronomical calculations for the entire year
    
    # Map alignment types to optimal dates
    optimal_date_map = {
        AlignmentType.SOLSTICE_WINTER: datetime(year, 12, 21),
        AlignmentType.SOLSTICE_SUMMER: datetime(year, 6, 21),
        AlignmentType.EQUINOX_SPRING: datetime(year, 3, 20),
        AlignmentType.EQUINOX_AUTUMN: datetime(year, 9, 22),
        AlignmentType.ZENITH: datetime(year, 8, 15) if site.culture == CultureType.HOPI else datetime(year, 5, 15),
        AlignmentType.RISING: datetime(year, 6, 15) if body == CelestialBody.PLEIADES else datetime(year, 7, 1)
    }
    
    # Get the optimal date if available, or use current date
    optimal_date = optimal_date_map.get(alignment_type, datetime(year, 1, 1))
    
    # Calculate alignment details for the optimal date
    alignment_details = target_alignment.calculate_for_date(
        optimal_date, site.location[0], site.location[1])
    
    return {
        "site": site.name,
        "alignment_type": alignment_type.value,
        "celestial_body": body.value,
        "optimal_date": optimal_date.isoformat(),
        "alignment_details": alignment_details,
        "seasonal_variations": target_alignment.seasonal_variations
    } 