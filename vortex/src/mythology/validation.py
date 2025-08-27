"""
Mythological Validation System

This module provides comprehensive validation for mythological accuracy across all systems.
It ensures proper relationships between deities, elements, cosmic levels, and cross-cultural
correspondences while maintaining historical and mythological accuracy.
"""

from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
from datetime import datetime

from . import (
    mayan, dogon, sufi, japanese, aboriginal, chinese, 
    greco_roman, hindu, norse, tatar, cross_cultural,
    sacred_geometry, celestial_alignments
)
from .result import ValidationResult

class ValidationLevel(Enum):
    """Levels of validation strictness."""
    STRICT = "strict"  # Must match exactly with historical sources
    FLEXIBLE = "flexible"  # Allows for some interpretation
    SYMBOLIC = "symbolic"  # Focuses on symbolic meaning rather than literal accuracy

class MythologyValidator:
    """Core validator for all mythological systems."""
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STRICT):
        self.validation_level = validation_level
        self.validation_cache = {}  # Cache validation results
        
    def validate_deity_attributes(self, deity_name: str, mythology: str) -> ValidationResult:
        """Validate a deity's attributes against historical sources."""
        issues = []
        suggestions = []
        confidence = 1.0
        sources = []
        
        # Get deity data from appropriate mythology module
        deity_data = self._get_deity_data(deity_name, mythology)
        if not deity_data:
            return ValidationResult(False, ["Deity not found"], [], 0.0, [])
            
        # Validate core attributes
        self._validate_core_attributes(deity_data, issues, suggestions, confidence)
        
        # Validate relationships with other deities
        self._validate_deity_relationships(deity_data, mythology, issues, suggestions)
        
        # Validate symbolic associations
        self._validate_symbolism(deity_data, mythology, issues, suggestions)
        
        # Check cross-cultural consistency
        self._validate_cross_cultural(deity_name, mythology, issues, suggestions)
        
        return ValidationResult(
            len(issues) == 0,
            issues,
            suggestions,
            confidence,
            sources
        )
    
    def validate_ritual_timing(self, ritual_name: str, timing: datetime, 
                             mythology: str) -> ValidationResult:
        """Validate ritual timing against astronomical and calendar alignments."""
        issues = []
        suggestions = []
        
        # Get ritual requirements
        ritual_data = self._get_ritual_data(ritual_name, mythology)
        if not ritual_data:
            return ValidationResult(False, ["Ritual not found"], [], 0.0, [])
            
        # Check celestial alignments
        celestial_valid = celestial_alignments.verify_alignment(
            timing, ritual_data.get("required_alignments", [])
        )
        if not celestial_valid:
            issues.append(f"Invalid celestial alignment for {ritual_name}")
            
        # Check calendar system validity
        calendar_valid = self._validate_calendar_timing(
            timing, ritual_data, mythology
        )
        if not calendar_valid:
            issues.append(f"Invalid calendar timing for {ritual_name}")
            
        return ValidationResult(
            len(issues) == 0,
            issues,
            suggestions,
            1.0 if len(issues) == 0 else 0.5,
            []
        )
    
    def validate_sacred_geometry(self, pattern_name: str, 
                               geometry_data: Dict) -> ValidationResult:
        """Validate sacred geometric patterns and proportions."""
        return sacred_geometry.validate_pattern(pattern_name, geometry_data)
    
    def _get_deity_data(self, deity_name: str, mythology: str) -> Optional[Dict]:
        """Retrieve deity data from the appropriate mythology module."""
        mythology_module = self._get_mythology_module(mythology)
        if not mythology_module:
            return None
        return getattr(mythology_module, "DEITIES", {}).get(deity_name)
    
    def _get_mythology_module(self, mythology: str):
        """Get the appropriate mythology module."""
        mythology_map = {
            "mayan": mayan,
            "dogon": dogon,
            "sufi": sufi,
            "japanese": japanese,
            "aboriginal": aboriginal,
            "chinese": chinese,
            "greco_roman": greco_roman,
            "hindu": hindu,
            "norse": norse,
            "tatar": tatar
        }
        return mythology_map.get(mythology)
    
    def _validate_core_attributes(self, deity_data: Dict, 
                                issues: List[str], 
                                suggestions: List[str],
                                confidence: float) -> None:
        """Validate core attributes of a deity."""
        required_attributes = {"role", "element", "symbol", "domain"}
        missing_attributes = required_attributes - set(deity_data.keys())
        
        if missing_attributes:
            issues.append(f"Missing required attributes: {missing_attributes}")
            confidence *= 0.8
            
        # Validate attribute relationships
        if "element" in deity_data and "domain" in deity_data:
            if not self._validate_element_domain_relationship(
                deity_data["element"], 
                deity_data["domain"]
            ):
                issues.append("Inconsistent element-domain relationship")
                suggestions.append(
                    f"Consider reviewing the relationship between "
                    f"{deity_data['element']} and {deity_data['domain']}"
                )
    
    def _validate_element_domain_relationship(self, 
                                           element: str, 
                                           domain: str) -> bool:
        """Validate the relationship between an element and domain."""
        # Implementation would contain extensive mapping of valid relationships
        return True  # Placeholder
    
    def _validate_deity_relationships(self, 
                                    deity_data: Dict,
                                    mythology: str,
                                    issues: List[str],
                                    suggestions: List[str]) -> None:
        """Validate relationships between deities."""
        mythology_module = self._get_mythology_module(mythology)
        if not mythology_module:
            return
            
        # Check pantheon relationships
        if hasattr(mythology_module, "DEITY_RELATIONSHIPS"):
            relationships = getattr(mythology_module, "DEITY_RELATIONSHIPS")
            # Validation logic for deity relationships would go here
            
    def _validate_symbolism(self, 
                          deity_data: Dict,
                          mythology: str,
                          issues: List[str],
                          suggestions: List[str]) -> None:
        """Validate symbolic associations."""
        if "symbol" in deity_data:
            symbol = deity_data["symbol"]
            shared_symbolism = cross_cultural.find_shared_symbolism(symbol)
            
            if shared_symbolism:
                if mythology in shared_symbolism:
                    if shared_symbolism[mythology] != deity_data.get("name"):
                        issues.append(f"Inconsistent symbol association: {symbol}")
                        
    def _validate_cross_cultural(self, 
                               deity_name: str,
                               mythology: str,
                               issues: List[str],
                               suggestions: List[str]) -> None:
        """Validate cross-cultural consistency."""
        for other_mythology in self._get_all_mythologies():
            if other_mythology == mythology:
                continue
                
            equivalent = cross_cultural.get_equivalent_deity(
                deity_name, 
                mythology, 
                other_mythology
            )
            
            if equivalent:
                # Validate equivalent deity attributes for consistency
                other_deity = self._get_deity_data(equivalent, other_mythology)
                if other_deity:
                    self._validate_equivalent_deities(
                        deity_name,
                        mythology,
                        equivalent,
                        other_mythology,
                        issues,
                        suggestions
                    )
    
    def _get_all_mythologies(self) -> List[str]:
        """Get list of all supported mythologies."""
        return [
            "mayan", "dogon", "sufi", "japanese", "aboriginal",
            "chinese", "greco_roman", "hindu", "norse", "tatar"
        ]
    
    def _validate_calendar_timing(self, 
                                timing: datetime,
                                ritual_data: Dict,
                                mythology: str) -> bool:
        """Validate timing against appropriate calendar system."""
        # Implementation would contain calendar system validation
        return True  # Placeholder 