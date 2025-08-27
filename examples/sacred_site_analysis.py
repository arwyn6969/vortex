#!/usr/bin/env python3
"""
Sacred Sites and Celestial Alignments Example

This example demonstrates how to use the sacred sites and alignment analysis
modules to explore astronomical alignments at ancient sites, with a focus
on Teotihuacan.
"""

import sys
from pprint import pprint
from datetime import datetime

# Add the project root to the Python path
sys.path.append(".")

from vortex.src.mythology import (
    CelestialBody,
    AlignmentType,
    get_site_by_name,
    get_sites_by_culture,
    get_sites_by_alignment,
    get_sites_with_zenith_passages,
    get_teotihuacan_info,
    SacredSite,
    AlignmentPattern,
    CrossCulturalAnalysis,
    MythologicalConnections,
    TeotihuacanAnalysis
)
from vortex.src.mythology.sacred_sites import CultureType

def main():
    """Run the sacred sites analysis example."""
    print("=" * 80)
    print("SACRED SITES AND CELESTIAL ALIGNMENTS ANALYSIS")
    print("=" * 80)
    
    # Analyze Teotihuacan
    print("\n\n" + "=" * 40)
    print("TEOTIHUACAN ANALYSIS")
    print("=" * 40)
    
    # Get detailed information about Teotihuacan
    teotihuacan_info = get_teotihuacan_info()
    print("\nTeotihuacan Overview:")
    print(f"Name: {teotihuacan_info['site'].name}")
    print(f"Location: {teotihuacan_info['site'].location}")
    print(f"Culture: {teotihuacan_info['site'].culture.value}")
    print(f"Date Range: {teotihuacan_info['site'].date_range[0]} to {teotihuacan_info['site'].date_range[1]} CE")
    
    # Display zenith passage information
    print("\nSun Zenith Passage Dates:")
    for date in teotihuacan_info["zenith_passage_dates"]["sun"]:
        print(f"  - {date}")
    
    # Display orientation information
    print(f"\nSite Orientation: {teotihuacan_info['avenue_of_dead_orientation']}")
    print("\nSignificant Alignments:")
    for alignment in teotihuacan_info["significant_alignments"]:
        print(f"  - {alignment}")
    
    # Analyze the North Star claim
    print("\n\n" + "=" * 40)
    print("NORTH STAR CLAIM ANALYSIS")
    print("=" * 40)
    
    north_star_analysis = TeotihuacanAnalysis.analyze_north_star_claim()
    print(f"\nClaim: {north_star_analysis['claim']}")
    print(f"Accuracy: {north_star_analysis['accuracy']}")
    print("\nExplanation:")
    print(north_star_analysis["explanation"])
    
    print("\nAstronomical Facts:")
    for fact in north_star_analysis["astronomical_facts"]:
        print(f"  - {fact}")
    
    # Find other sites with zenith passages
    print("\n\n" + "=" * 40)
    print("ALL SITES WITH ZENITH PASSAGES")
    print("=" * 40)
    
    zenith_sites = get_sites_with_zenith_passages()
    print(f"\nFound {len(zenith_sites)} sites with zenith passages:")
    for site in zenith_sites:
        print(f"  - {site.name} ({site.culture.value}): {site.zenith_passages}")
    
    # Compare Teotihuacan with other Mesoamerican sites
    print("\n\n" + "=" * 40)
    print("COMPARISON WITH CHICHEN ITZA")
    print("=" * 40)
    
    comparison = CrossCulturalAnalysis.compare_sites("teotihuacan", "chichen_itza")
    
    print(f"\nComparing {comparison['site1']} ({comparison['culture1']}) and "
          f"{comparison['site2']} ({comparison['culture2']})")
    
    print("\nShared Alignments:")
    for alignment in comparison["shared_alignments"]:
        print(f"  - Type: {alignment['type']}, Body: {alignment['body']}")
    
    print("\nUnique Alignments at Teotihuacan:")
    for alignment in comparison["unique_alignments"]["Teotihuacan"]:
        print(f"  - Type: {alignment['type']}, Body: {alignment['body']}")
    
    print("\nUnique Alignments at Chichen Itza:")
    for alignment in comparison["unique_alignments"]["Chichen Itza"]:
        print(f"  - Type: {alignment['type']}, Body: {alignment['body']}")
    
    print("\nShared Mythological Themes:")
    for theme in comparison["shared_mythological_themes"]:
        print(f"  - Mythology: {theme['mythology']}")
        print(f"    - At Teotihuacan: {theme['Teotihuacan']}")
        print(f"    - At Chichen Itza: {theme['Chichen Itza']}")
    
    # Find all solar-aligned sites
    print("\n\n" + "=" * 40)
    print("SOLAR-ALIGNED SITES")
    print("=" * 40)
    
    solar_sites = get_sites_by_alignment(AlignmentType.ZENITH, CelestialBody.SUN)
    solar_sites += get_sites_by_alignment(AlignmentType.SOLSTICE_SUMMER, CelestialBody.SUN)
    solar_sites += get_sites_by_alignment(AlignmentType.SOLSTICE_WINTER, CelestialBody.SUN)
    solar_sites += get_sites_by_alignment(AlignmentType.EQUINOX_SPRING, CelestialBody.SUN)
    
    # Remove duplicates
    unique_solar_sites = []
    site_names = set()
    for site in solar_sites:
        if site.name not in site_names:
            site_names.add(site.name)
            unique_solar_sites.append(site)
    
    print(f"\nFound {len(unique_solar_sites)} sites with solar alignments:")
    for site in unique_solar_sites:
        print(f"  - {site.name} ({site.culture.value})")
    
    # Find sites associated with creation myths
    print("\n\n" + "=" * 40)
    print("CREATION MYTH SITES")
    print("=" * 40)
    
    creation_sites = MythologicalConnections.get_creation_sites()
    print(f"\nFound {len(creation_sites)} sites associated with creation myths:")
    for site in creation_sites:
        for mythology, connection in site.mythological_connections.items():
            if any(term in connection.lower() for term in ["creation", "born", "emerge", "origin"]):
                print(f"  - {site.name} ({mythology}): {connection}")
    
    # Find all sites with solar deity connections
    print("\n\n" + "=" * 40)
    print("SOLAR DEITY SITES")
    print("=" * 40)
    
    solar_deity_sites = MythologicalConnections.get_solar_deity_sites()
    print("\nSites associated with solar deities by mythology:")
    for mythology, sites in solar_deity_sites.items():
        print(f"\n{mythology.capitalize()} solar sites:")
        for site_name in sites:
            print(f"  - {site_name}")
    
    # Find cosmic axis (axis mundi) sites
    print("\n\n" + "=" * 40)
    print("COSMIC AXIS (AXIS MUNDI) SITES")
    print("=" * 40)
    
    axis_sites = AlignmentPattern.find_axis_mundi_sites()
    print(f"\nFound {len(axis_sites)} sites representing the cosmic axis:")
    for site in axis_sites:
        print(f"  - {site.name} ({site.culture.value})")
        
    # Compare common alignments across cultures
    print("\n\n" + "=" * 40)
    print("CROSS-CULTURAL ALIGNMENT PATTERNS")
    print("=" * 40)
    
    all_sites = list(get_sites_by_culture(CultureType.MAYAN))
    all_sites += list(get_sites_by_culture(CultureType.AZTEC))
    all_sites += list(get_sites_by_culture(CultureType.EGYPTIAN))
    
    common_alignments = AlignmentPattern.find_common_alignments(all_sites)
    
    print(f"\nFound {len(common_alignments)} common alignment patterns across cultures:")
    for pattern, sites in common_alignments.items():
        alignment_type, body = pattern.split('_')
        print(f"\n{alignment_type.capitalize()} of {body}:")
        for site in sites:
            print(f"  - {site.name} ({site.culture.value})")

if __name__ == "__main__":
    main() 