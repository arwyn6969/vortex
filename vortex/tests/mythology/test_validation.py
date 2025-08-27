"""
Test suite for the mythology validation system.
"""

import pytest
from datetime import datetime
from vortex.src.mythology.validation import (
    MythologyValidator,
    ValidationLevel,
    ValidationResult
)

@pytest.fixture
def validator():
    """Create a validator instance for testing."""
    return MythologyValidator(validation_level=ValidationLevel.STRICT)

class TestDeityValidation:
    """Test suite for deity validation functionality."""
    
    def test_valid_mayan_deity(self, validator):
        """Test validation of a well-formed Mayan deity."""
        result = validator.validate_deity_attributes("itzamna", "mayan")
        assert result.is_valid
        assert result.confidence_score > 0.9
        assert not result.issues
        
    def test_valid_dogon_deity(self, validator):
        """Test validation of a well-formed Dogon deity."""
        result = validator.validate_deity_attributes("nommo", "dogon")
        assert result.is_valid
        assert result.confidence_score > 0.9
        assert not result.issues
        
    def test_invalid_deity(self, validator):
        """Test validation of a non-existent deity."""
        result = validator.validate_deity_attributes("nonexistent", "mayan")
        assert not result.is_valid
        assert "Deity not found" in result.issues
        
    def test_missing_attributes(self, validator):
        """Test validation of a deity with missing attributes."""
        # This would require mocking the deity data to simulate missing attributes
        pass
        
    def test_cross_cultural_validation(self, validator):
        """Test cross-cultural validation of equivalent deities."""
        # Test Mayan Kukulcan with Aztec Quetzalcoatl
        result = validator.validate_deity_attributes("kukulcan", "mayan")
        assert result.is_valid
        assert result.confidence_score > 0.8
        
class TestRitualValidation:
    """Test suite for ritual timing validation."""
    
    def test_valid_ritual_timing(self, validator):
        """Test validation of correctly timed ritual."""
        timing = datetime(2024, 3, 20, 12, 0)  # Spring equinox
        result = validator.validate_ritual_timing(
            "spring_ceremony",
            timing,
            "mayan"
        )
        assert result.is_valid
        assert not result.issues
        
    def test_invalid_ritual_timing(self, validator):
        """Test validation of incorrectly timed ritual."""
        timing = datetime(2024, 1, 1, 12, 0)  # Not an significant date
        result = validator.validate_ritual_timing(
            "spring_ceremony",
            timing,
            "mayan"
        )
        assert not result.is_valid
        assert "Invalid celestial alignment" in result.issues[0]
        
    def test_calendar_system_validation(self, validator):
        """Test validation against specific calendar systems."""
        # Test Mayan Tzolkin calendar alignment
        timing = datetime(2024, 3, 20, 12, 0)
        result = validator.validate_ritual_timing(
            "tzolkin_ceremony",
            timing,
            "mayan"
        )
        assert result.is_valid
        
class TestGeometryValidation:
    """Test suite for sacred geometry validation."""
    
    def test_valid_geometry_pattern(self, validator):
        """Test validation of correct geometric pattern."""
        pattern_data = {
            "type": "flower_of_life",
            "circles": 7,
            "radius_ratio": 1.0
        }
        result = validator.validate_sacred_geometry(
            "flower_of_life",
            pattern_data
        )
        assert result.is_valid
        assert result.confidence_score > 0.9
        
    def test_invalid_geometry_pattern(self, validator):
        """Test validation of incorrect geometric pattern."""
        pattern_data = {
            "type": "flower_of_life",
            "circles": 4,  # Invalid number
            "radius_ratio": 0.5  # Invalid ratio
        }
        result = validator.validate_sacred_geometry(
            "flower_of_life",
            pattern_data
        )
        assert not result.is_valid
        assert "Invalid circle count" in result.issues
        
class TestValidationLevels:
    """Test suite for different validation levels."""
    
    def test_strict_validation(self):
        """Test strict validation level."""
        validator = MythologyValidator(ValidationLevel.STRICT)
        result = validator.validate_deity_attributes("itzamna", "mayan")
        assert result.is_valid  # Should pass with exact historical match
        
    def test_flexible_validation(self):
        """Test flexible validation level."""
        validator = MythologyValidator(ValidationLevel.FLEXIBLE)
        result = validator.validate_deity_attributes("itzamna", "mayan")
        assert result.is_valid  # Should allow some interpretation
        
    def test_symbolic_validation(self):
        """Test symbolic validation level."""
        validator = MythologyValidator(ValidationLevel.SYMBOLIC)
        result = validator.validate_deity_attributes("itzamna", "mayan")
        assert result.is_valid  # Should focus on symbolic meaning
        
class TestCrossCulturalValidation:
    """Test suite for cross-cultural validation."""
    
    def test_equivalent_deities(self, validator):
        """Test validation of equivalent deities across cultures."""
        # Test equivalent creator deities
        mayan_result = validator.validate_deity_attributes("itzamna", "mayan")
        dogon_result = validator.validate_deity_attributes("amma", "dogon")
        
        assert mayan_result.is_valid and dogon_result.is_valid
        # They should have similar confidence scores as equivalent deities
        assert abs(mayan_result.confidence_score - dogon_result.confidence_score) < 0.1
        
    def test_shared_symbols(self, validator):
        """Test validation of shared symbolic meanings."""
        # Test serpent symbolism across cultures
        result = validator.validate_deity_attributes("kukulcan", "mayan")
        assert result.is_valid
        assert "serpent" in str(result.source_references)
        
class TestValidationCache:
    """Test suite for validation result caching."""
    
    def test_cache_hit(self, validator):
        """Test that validation results are properly cached."""
        # First validation
        result1 = validator.validate_deity_attributes("itzamna", "mayan")
        # Second validation should use cache
        result2 = validator.validate_deity_attributes("itzamna", "mayan")
        
        assert result1.is_valid == result2.is_valid
        assert result1.confidence_score == result2.confidence_score
        
    def test_cache_invalidation(self, validator):
        """Test that cache is properly invalidated."""
        # This would require implementing and testing cache invalidation logic
        pass 