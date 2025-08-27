#!/usr/bin/env python3
"""
Simplified Sacred Site Alignment Demo

This script demonstrates the enhanced sacred site alignment functionality
for Syrian alchemical sites and Hopi kiva alignments without relying on
the mythology package's imports to avoid circular import issues.
"""

import sys
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
import json

# Add the parent directory to the path so we can import the modules directly
sys.path.append('..')

class SiteDemo:
    """Demonstration class for sacred site alignments."""
    
    def __init__(self):
        # Import the needed classes directly to avoid circular imports
        from vortex.src.mythology.celestial_alignments import CelestialBody, AlignmentType
        from vortex.src.mythology.sacred_sites import SiteType, CultureType
        
        # Store them as class attributes
        self.CelestialBody = CelestialBody
        self.AlignmentType = AlignmentType
        self.SiteType = SiteType
        self.CultureType = CultureType
    
    def print_section(self, title: str) -> None:
        """Print a section header."""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    
    def print_json(self, data: Dict) -> None:
        """Print data as formatted JSON."""
        print(json.dumps(data, indent=2, default=str))
    
    def show_site_info(self, site_name: str) -> None:
        """Display basic information about a sacred site."""
        from vortex.src.mythology.sacred_sites import get_site_by_name
        
        site = get_site_by_name(site_name)
        if site:
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
        else:
            print(f"Site '{site_name}' not found.")
    
    def calculate_alignments(self, site_name: str, date: datetime) -> None:
        """Calculate alignments for a site on a specific date."""
        from vortex.src.mythology.sacred_sites import calculate_site_alignments_for_date
        
        alignments = calculate_site_alignments_for_date(site_name, date)
        print(f"\nAlignments for {site_name} on {date.date()}:")
        self.print_json(alignments)
    
    def show_syrian_sites(self) -> None:
        """Show Syrian alchemical sites."""
        self.print_section("SYRIAN ALCHEMICAL SITES")
        
        from vortex.src.mythology.sacred_sites import get_syrian_alchemical_sites
        
        sites = get_syrian_alchemical_sites()
        print(f"Found {len(sites)} Syrian alchemical sites:")
        for site in sites:
            print(f"- {site.name} ({site.site_type.value})")
            print(f"  Location: {site.location}")
            print(f"  Date Range: {site.date_range}")
            print(f"  Number of alignments: {len(site.alignments)}")
            print()
    
    def show_hopi_sites(self) -> None:
        """Show Hopi sites."""
        self.print_section("HOPI SITES")
        
        from vortex.src.mythology.sacred_sites import get_hopi_sites
        
        sites = get_hopi_sites()
        print(f"Found {len(sites)} Hopi sites:")
        for site in sites:
            print(f"- {site.name} ({site.site_type.value})")
            print(f"  Location: {site.location}")
            print(f"  Date Range: {site.date_range}")
            print(f"  Number of alignments: {len(site.alignments)}")
            print()
    
    def analyze_site_alignments(self, site_name: str) -> None:
        """Analyze alignments for a specific site."""
        self.print_section(f"ALIGNMENT ANALYSIS FOR {site_name.upper()}")
        
        from vortex.src.mythology.sacred_sites import get_site_by_name
        
        site = get_site_by_name(site_name)
        if not site:
            print(f"Site '{site_name}' not found.")
            return
        
        # Show all alignments
        print("Alignments:")
        for idx, alignment in enumerate(site.alignments, 1):
            print(f"{idx}. {alignment.alignment_type.value} of {alignment.primary_body.value}")
            if alignment.secondary_body:
                print(f"   with {alignment.secondary_body.value}")
            print(f"   Significance: {alignment.cultural_significance}")
            
            # Show seasonal variations if available
            if hasattr(alignment, 'seasonal_variations') and alignment.seasonal_variations:
                print("   Seasonal Variations:")
                for season, description in alignment.seasonal_variations.items():
                    print(f"     - {season.capitalize()}: {description}")
            
            # Show mathematical model if available
            if hasattr(alignment, 'math_model') and alignment.math_model:
                print("   Has mathematical model: Yes")
                print(f"     Seasonal variation: {alignment.math_model.seasonal_variation} degrees")
                print(f"     Epoch shift: {alignment.math_model.epoch_shift} degrees/century")
            else:
                print("   Has mathematical model: No")
            
            print()
    
    def calculate_alignment_for_dates(self, site_name: str) -> None:
        """Calculate alignments for key dates."""
        self.print_section(f"ALIGNMENT CALCULATIONS FOR {site_name.upper()}")
        
        # Key astronomical dates in 2023
        dates = [
            datetime(2023, 12, 21),  # Winter solstice
            datetime(2023, 6, 21),   # Summer solstice
            datetime(2023, 3, 20),   # Spring equinox
            datetime(2023, 9, 22),   # Fall equinox
            datetime.now()           # Current date
        ]
        
        for date in dates:
            self.calculate_alignments(site_name, date)
            print("\n" + "-" * 40 + "\n")
    
    def run_demo(self) -> None:
        """Run the complete demonstration."""
        self.print_section("SACRED SITE ALIGNMENT DEMONSTRATION")
        print("This script demonstrates the alignment functionality for Syrian and Hopi sacred sites.")
        
        # Show Syrian sites
        self.show_syrian_sites()
        
        # Show Hopi sites
        self.show_hopi_sites()
        
        # Show detailed information for specific sites
        self.print_section("DETAILED SITE INFORMATION")
        
        syrian_site = "Harran Sabians Complex"
        self.show_site_info(syrian_site)
        
        print("\n" + "-" * 40 + "\n")
        
        hopi_site = "Walpi Village"
        self.show_site_info(hopi_site)
        
        # Analyze alignments for both sites
        self.analyze_site_alignments(syrian_site)
        self.analyze_site_alignments(hopi_site)
        
        # Calculate alignments for key dates
        self.calculate_alignment_for_dates(syrian_site)
        self.calculate_alignment_for_dates(hopi_site)
        
        self.print_section("DEMONSTRATION COMPLETED")
        print("The sacred site alignment functionality has been successfully demonstrated.")

if __name__ == "__main__":
    demo = SiteDemo()
    demo.run_demo() 