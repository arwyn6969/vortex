"""
Tests for the configuration management system.
"""
import os
import json
import pytest
from pathlib import Path
import tempfile
from unittest.mock import patch

from vortex.src.core.config import config, ConfigManager, ConfigValidationError, ConfigType


class TestConfigManager:
    """Test suite for the ConfigManager class."""

    def test_get_default_values(self):
        """Test getting default configuration values."""
        # Reset to defaults
        config.reset_to_defaults()
        
        # Test app configuration
        assert config.get("app.name") == "VORTEX"
        assert config.get("app.version") == "0.1.0"
        assert config.get("app.debug") is False
        
        # Test database configuration
        assert config.get("database.url") == "sqlite:///vortex.db"
        assert config.get("database.pool_size") == 5
        
        # Test LLM configuration
        assert config.get("llm.temperature") == 0.7
        assert config.get("llm.retry_attempts") == 3
        
        # Test default return for non-existent keys
        assert config.get("non_existent.key") is None
        assert config.get("non_existent.key", "default") == "default"
        
        # Test invalid key format
        assert config.get("invalid_key_format") is None

    def test_set_and_get_values(self):
        """Test setting and getting configuration values."""
        # Reset to defaults
        config.reset_to_defaults()
        
        # Set new values
        config.set("app.debug", True)
        config.set("database.url", "postgresql://localhost/vortex")
        config.set("llm.temperature", 0.5)
        
        # Create a new category
        config.set("custom.value", "test")
        
        # Verify values
        assert config.get("app.debug") is True
        assert config.get("database.url") == "postgresql://localhost/vortex"
        assert config.get("llm.temperature") == 0.5
        assert config.get("custom.value") == "test"
        
        # Test invalid key format
        with pytest.raises(ValueError):
            config.set("invalid_key_format", "value")

    def test_has_config(self):
        """Test checking if configuration exists."""
        # Reset to defaults
        config.reset_to_defaults()
        
        # Check existing keys
        assert config.has("app.name") is True
        assert config.has("database.url") is True
        
        # Check non-existent keys
        assert config.has("non_existent.key") is False
        
        # Check invalid key format
        assert config.has("invalid_key_format") is False
        
        # Add a new key and check again
        config.set("custom.value", "test")
        assert config.has("custom.value") is True

    def test_validation(self):
        """Test configuration validation."""
        # Reset to defaults
        config.reset_to_defaults()
        
        # Test valid values
        config.set("llm.temperature", 0.3)  # Valid: 0 <= x <= 1
        assert config.get("llm.temperature") == 0.3
        
        config.set("llm.max_tokens", 100)  # Valid: x > 0
        assert config.get("llm.max_tokens") == 100
        
        # Test invalid values
        with pytest.raises(ConfigValidationError):
            config.set("llm.temperature", 1.5)  # Invalid: > 1.0
            
        with pytest.raises(ConfigValidationError):
            config.set("llm.temperature", -0.1)  # Invalid: < 0.0
            
        with pytest.raises(ConfigValidationError):
            config.set("llm.max_tokens", 0)  # Invalid: not > 0
            
        with pytest.raises(ConfigValidationError):
            config.set("security.password_min_length", 5)  # Invalid: < 6

    def test_get_all(self):
        """Test getting all configuration values."""
        # Reset to defaults
        config.reset_to_defaults()
        
        # Get all values
        all_config = config.get_all()
        assert isinstance(all_config, dict)
        assert "app.name" in all_config
        assert "database.url" in all_config
        
        # Get category-specific values
        db_config = config.get_all("database")
        assert isinstance(db_config, dict)
        assert "url" in db_config
        assert "pool_size" in db_config
        
        # Get non-existent category
        non_existent = config.get_all("non_existent")
        assert non_existent == {}

    def test_load_from_file(self):
        """Test loading configuration from a file."""
        # Create a temporary config file
        config_data = {
            "app": {
                "name": "VORTEX_TEST",
                "debug": True
            },
            "database": {
                "url": "sqlite:///test.db"
            },
            "custom": {
                "value": "from_file"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp:
            json.dump(config_data, temp)
            temp_path = temp.name
            
        try:
            # Reset to defaults
            config.reset_to_defaults()
            
            # Load from file
            assert config.load_from_file(temp_path) is True
            
            # Verify values
            assert config.get("app.name") == "VORTEX_TEST"
            assert config.get("app.debug") is True
            assert config.get("database.url") == "sqlite:///test.db"
            assert config.get("custom.value") == "from_file"
            
            # Verify default values still exist for unspecified keys
            assert config.get("llm.temperature") == 0.7
            
            # Test loading from non-existent file
            assert config.load_from_file("non_existent_file.json") is False
            
            # Test loading from invalid file (create empty file)
            with open(temp_path, "w") as f:
                f.write("not json")
            assert config.load_from_file(temp_path) is False
            
        finally:
            # Clean up
            os.unlink(temp_path)

    def test_save_to_file(self):
        """Test saving configuration to a file."""
        # Reset to defaults
        config.reset_to_defaults()
        
        # Set some custom values
        config.set("app.name", "VORTEX_SAVE_TEST")
        config.set("custom.value", "save_test")
        
        # Create temporary path
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "config.json"
            
            # Save to file
            assert config.save_to_file(temp_path) is True
            
            # Verify file exists
            assert temp_path.exists()
            
            # Verify file contents
            with open(temp_path, "r") as f:
                saved_data = json.load(f)
                
            assert saved_data["app"]["name"] == "VORTEX_SAVE_TEST"
            assert saved_data["custom"]["value"] == "save_test"
            
            # Test saving to invalid path
            assert config.save_to_file("/invalid/path/config.json") is False

    def test_reset_to_defaults(self):
        """Test resetting configuration to defaults."""
        # Set custom values
        config.set("app.name", "CUSTOM_NAME")
        config.set("database.url", "custom_url")
        config.set("custom.value", "custom")
        
        # Reset specific category
        config.reset_to_defaults("app")
        
        # Verify app settings were reset
        assert config.get("app.name") == "VORTEX"
        
        # Verify other settings remain
        assert config.get("database.url") == "custom_url"
        assert config.get("custom.value") == "custom"
        
        # Reset all settings
        config.reset_to_defaults()
        
        # Verify all settings were reset
        assert config.get("app.name") == "VORTEX"
        assert config.get("database.url") == "sqlite:///vortex.db"
        assert config.get("custom.value") is None

    @patch.dict(os.environ, {
        "VORTEX_APP__NAME": "ENV_VORTEX",
        "VORTEX_APP__DEBUG": "true",
        "VORTEX_DATABASE__URL": "sqlite:///env.db",
        "VORTEX_LLM__TEMPERATURE": "0.4",
        "VORTEX_LLM__MAX_TOKENS": "200",
        "VORTEX_CUSTOM__ENV_VALUE": "from_env",
        "VORTEX_INVALID": "not_used"  # Missing double underscore
    })
    def test_env_variables(self):
        """Test loading configuration from environment variables."""
        # Create a new instance to load from env
        test_config = ConfigManager()
        
        # Verify environment values were loaded
        assert test_config.get("app.name") == "ENV_VORTEX"
        assert test_config.get("app.debug") is True
        assert test_config.get("database.url") == "sqlite:///env.db"
        assert test_config.get("llm.temperature") == 0.4
        assert test_config.get("llm.max_tokens") == 200
        assert test_config.get("custom.env_value") == "from_env"
        
        # The invalid format key should not be loaded
        assert not test_config.has("invalid")

    @patch.dict(os.environ, {
        "VORTEX_LLM__TEMPERATURE": "2.0",  # Invalid: > 1.0
        "VORTEX_LLM__MAX_TOKENS": "0",      # Invalid: not > 0
        "VORTEX_SECURITY__PASSWORD_MIN_LENGTH": "3"  # Invalid: < 6
    })
    def test_env_validation(self):
        """Test validation of environment variables."""
        # Create a new instance to load from env
        test_config = ConfigManager()
        
        # Invalid values should not be loaded, defaults should remain
        assert test_config.get("llm.temperature") == 0.7
        assert test_config.get("llm.max_tokens") == 512
        assert test_config.get("security.password_min_length") == 8

    @patch.dict(os.environ, {
        "VORTEX_APP__DEBUG": "yes",         # Boolean
        "VORTEX_LLM__TEMPERATURE": "0.5",   # Float
        "VORTEX_LLM__MAX_TOKENS": "200",    # Integer
        "VORTEX_LLM__STOP_SEQUENCES": "[\"User:\", \"Human:\"]",  # JSON list
        "VORTEX_CUSTOM__DICT": "{\"key\": \"value\"}"  # JSON dict
    })
    def test_type_conversion(self):
        """Test type conversion of environment variables."""
        # Create a new instance to load from env
        test_config = ConfigManager()
        
        # Verify types were converted correctly
        assert isinstance(test_config.get("app.debug"), bool)
        assert test_config.get("app.debug") is True
        
        assert isinstance(test_config.get("llm.temperature"), float)
        assert test_config.get("llm.temperature") == 0.5
        
        assert isinstance(test_config.get("llm.max_tokens"), int)
        assert test_config.get("llm.max_tokens") == 200
        
        assert isinstance(test_config.get("llm.stop_sequences"), list)
        assert test_config.get("llm.stop_sequences") == ["User:", "Human:"]
        
        assert isinstance(test_config.get("custom.dict"), dict)
        assert test_config.get("custom.dict") == {"key": "value"} 