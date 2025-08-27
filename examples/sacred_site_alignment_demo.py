#!/usr/bin/env python3
"""
Sacred Site Alignment Demo

This script demonstrates the enhanced sacred site alignment functionality,
focusing particularly on Syrian alchemical sites and Hopi kiva alignments.
It shows how to calculate alignments for specific dates, find optimal
observation times, and analyze cultural patterns in astronomical alignments.
"""

import sys
from datetime import datetime
from typing import Dict, List, Optional
import json

# Add the parent directory to the path so we can import the vortex module
sys.path.append('..')

# Import directly from specific modules to avoid circular imports
from vortex.src.mythology.sacred_sites import (
    get_site_by_name, get_sites_by_culture, get_syrian_alchemical_sites, get_hopi_sites,
    calculate_site_alignments_for_date, get_alignment_seasonal_variation,
    SiteType, CultureType
)
from vortex.src.mythology.celestial_alignments import CelestialBody, AlignmentType
from vortex.src.mythology.alignment_analysis import (
    AlignmentPattern, CrossCulturalAnalysis, 
    SyrianAlchemicalAnalysis, HopiSiteAnalysis,
    calculate_alignment_accuracy, find_optimal_observation_date
)

def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_json(data: Dict) -> None:
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2, default=str))

def demonstrate_basic_site_info() -> None:
    """Demonstrate basic site information retrieval."""
    print_section("BASIC SITE INFORMATION")
    
    # Get information about a Syrian alchemical site
    harran_site = get_site_by_name("Harran Sabians Complex")
    if harran_site:
        print(f"Site: {harran_site.name}")
        print(f"Culture: {harran_site.culture.value}")
        print(f"Location: {harran_site.location}")
        print(f"Date Range: {harran_site.date_range}")
        print("\nAlignments:")
        for alignment in harran_site.alignments:
            print(f"  - {alignment.alignment_type.value} of {alignment.primary_body.value}")
            if alignment.secondary_body:
                print(f"    with {alignment.secondary_body.value}")
            print(f"    Significance: {alignment.cultural_significance}")
        
        print("\nMythological Connections:")
        for mythology, connection in harran_site.mythological_connections.items():
            print(f"  - {mythology}: {connection}")
    
    # Get information about a Hopi site
    walpi_site = get_site_by_name("Walpi Village")
    if walpi_site:
        print("\n\nSite: {walpi_site.name}")
        print(f"Culture: {walpi_site.culture.value}")
        print(f"Location: {walpi_site.location}")
        print(f"Date Range: {walpi_site.date_range}")
        print("\nAlignments:")
        for alignment in walpi_site.alignments:
            print(f"  - {alignment.alignment_type.value} of {alignment.primary_body.value}")
            print(f"    Significance: {alignment.cultural_significance}")

def demonstrate_alignment_calculations() -> None:
    """Demonstrate alignment calculations for specific dates."""
    print_section("ALIGNMENT CALCULATIONS FOR SPECIFIC DATES")
    
    # Calculate alignments for winter solstice
    winter_solstice = datetime(2023, 12, 21)
    print(f"Winter Solstice Alignments ({winter_solstice.date()}):")
    
    # Calculate for a Hopi site
    hopi_site = "Shungopavi Snake Kiva"
    hopi_alignments = calculate_site_alignments_for_date(hopi_site, winter_solstice)
    print(f"\n{hopi_site}:")
    print_json(hopi_alignments)
    
    # Calculate for a Syrian alchemical site
    syrian_site = "Aleppo Citadel Alchemical Chambers"
    syrian_alignments = calculate_site_alignments_for_date(syrian_site, winter_solstice)
    print(f"\n{syrian_site}:")
    print_json(syrian_alignments)
    
    # Calculate for summer solstice
    summer_solstice = datetime(2023, 6, 21)
    print(f"\n\nSummer Solstice Alignments ({summer_solstice.date()}):")
    
    # Calculate for the same sites
    hopi_summer_alignments = calculate_site_alignments_for_date(hopi_site, summer_solstice)
    print(f"\n{hopi_site}:")
    print_json(hopi_summer_alignments)
    
    syrian_summer_alignments = calculate_site_alignments_for_date(syrian_site, summer_solstice)
    print(f"\n{syrian_site}:")
    print_json(syrian_summer_alignments)

def demonstrate_seasonal_variations() -> None:
    """Demonstrate seasonal variations in alignments."""
    print_section("SEASONAL VARIATIONS IN ALIGNMENTS")
    
    # Get sites with seasonal variations
    sites_with_variations = AlignmentPattern.find_sites_with_seasonal_variations()
    
    print("Sites with documented seasonal variations:")
    for site_name, variations in sites_with_variations.items():
        print(f"\n{site_name}:")
        for season, alignments in variations.items():
            print(f"  {season.capitalize()}:")
            for alignment in alignments:
                print(f"    - {alignment}")
    
    # Get detailed seasonal variations for a specific alignment
    print("\nDetailed seasonal variations for a specific alignment:")
    walpi_variations = get_alignment_seasonal_variation(
        "Walpi Village", 
        AlignmentType.SOLSTICE_WINTER, 
        CelestialBody.SUN
    )
    print(f"Walpi Village - Winter Solstice Sun:")
    print_json(walpi_variations)

def demonstrate_alchemical_analysis() -> None:
    """Demonstrate Syrian alchemical site analysis."""
    print_section("SYRIAN ALCHEMICAL SITE ANALYSIS")
    
    # Get all Syrian alchemical sites
    syrian_sites = get_syrian_alchemical_sites()
    print(f"Syrian Alchemical Sites: {[site.name for site in syrian_sites]}")
    
    # Analyze alchemical stages
    stages_analysis = SyrianAlchemicalAnalysis.analyze_alchemical_stages()
    print("\nAlchemical Stages Analysis:")
    print_json(stages_analysis)
    
    # Analyze optimal times for alchemical operations
    current_date = datetime.now()
    operations_analysis = SyrianAlchemicalAnalysis.analyze_alchemical_operations(current_date)
    print("\nAlchemical Operations Analysis for Current Date:")
    print_json(operations_analysis)
    
    # Find optimal dates for calcination in 2023
    calcination_dates = SyrianAlchemicalAnalysis.find_optimal_alchemical_dates(2023, "calcination")
    print("\nOptimal Dates for Calcination in 2023:")
    print_json(calcination_dates[:3])  # Show just the first 3 dates

def demonstrate_hopi_analysis() -> None:
    """Demonstrate Hopi site analysis."""
    print_section("HOPI SITE ANALYSIS")
    
    # Get all Hopi sites
    hopi_sites = get_hopi_sites()
    print(f"Hopi Sites: {[site.name for site in hopi_sites]}")
    
    # Analyze directional symbolism
    direction_analysis = HopiSiteAnalysis.analyze_directional_symbolism()
    print("\nDirectional Symbolism Analysis:")
    print_json(direction_analysis)
    
    # Analyze kiva alignments for winter solstice
    winter_solstice = datetime(2023, 12, 21)
    kiva_analysis = HopiSiteAnalysis.analyze_kiva_alignments(winter_solstice)
    print("\nKiva Alignments Analysis for Winter Solstice:")
    print_json(kiva_analysis)
    
    # Analyze world cycles representation
    cycles_analysis = HopiSiteAnalysis.analyze_world_cycles_representation()
    print("\nWorld Cycles Representation Analysis:")
    print_json(cycles_analysis)

def demonstrate_cross_cultural_comparison() -> None:
    """Demonstrate cross-cultural comparison of sites."""
    print_section("CROSS-CULTURAL COMPARISON")
    
    # Compare a Syrian alchemical site with a Hopi site
    comparison = CrossCulturalAnalysis.compare_sites(
        "Harran Sabians Complex",
        "Walpi Village"
    )
    print("Comparison between Syrian Alchemical and Hopi sites:")
    print_json(comparison)
    
    # Compare their mathematical models for winter solstice
    winter_solstice = datetime(2023, 12, 21)
    model_comparison = CrossCulturalAnalysis.compare_mathematical_models(
        "Harran Sabians Complex",
        "Walpi Village", 
        winter_solstice
    )
    print("\nMathematical Model Comparison for Winter Solstice:")
    print_json(model_comparison)

def demonstrate_finding_optimal_dates() -> None:
    """Demonstrate finding optimal observation dates."""
    print_section("FINDING OPTIMAL OBSERVATION DATES")
    
    # Find optimal date to observe winter solstice at a Hopi site
    hopi_optimal = find_optimal_observation_date(
        "Shungopavi Snake Kiva",
        AlignmentType.SOLSTICE_WINTER,
        CelestialBody.SUN,
        2023
    )
    print("Optimal date to observe winter solstice at Shungopavi Snake Kiva:")
    print_json(hopi_optimal)
    
    # Find optimal date to observe Mercury rising at a Syrian site
    syrian_optimal = find_optimal_observation_date(
        "Harran Sabians Complex",
        AlignmentType.RISING,
        CelestialBody.MERCURY,
        2023
    )
    print("\nOptimal date to observe Mercury rising at Harran Sabians Complex:")
    print_json(syrian_optimal)

def main() -> None:
    """Run the demonstration script."""
    print("\nSACRED SITE ALIGNMENT DEMONSTRATION")
    print("This script demonstrates sacred site alignments, with a focus on")
    print("Syrian alchemical and Hopi traditions and their celestial alignments.")
    
    demonstrate_basic_site_info()
    demonstrate_alignment_calculations()
    demonstrate_seasonal_variations()
    demonstrate_alchemical_analysis()
    demonstrate_hopi_analysis()
    demonstrate_cross_cultural_comparison()
    demonstrate_finding_optimal_dates()
    
    print("\nDemonstration completed. For detailed analysis, please refer to the")
    print("documentation or use the module functions in your own code.")

if __name__ == "__main__":
    main() 