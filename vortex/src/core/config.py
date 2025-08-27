"""
Configuration management system for the VORTEX application.

This module provides centralized configuration handling with support for:
- Default configuration values
- Environment variable overrides
- Configuration validation
- Type conversion
- Configuration categories

Usage example:
    from vortex.src.core.config import config
    
    # Access configuration values
    db_url = config.get("database.url")
    debug_mode = config.get("app.debug", default=False)
    
    # Check if a configuration exists
    if config.has("llm.api_key"):
        # Use the API key
        api_key = config.get("llm.api_key")
"""

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Set, Tuple, cast
from enum import Enum

logger = logging.getLogger(__name__)


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


class ConfigType(Enum):
    """Enum for configuration value types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"


class ConfigManager:
    """
    Central configuration management system for VORTEX.
    
    Handles configuration loading, validation, and access with support
    for environment variable overrides and type conversion.
    """
    
    def __init__(self):
        """Initialize the configuration manager with default settings."""
        self._config: Dict[str, Dict[str, Any]] = {
            "app": {
                "name": "VORTEX",
                "version": "0.1.0",
                "debug": False,
                "log_level": "INFO",
            },
            "database": {
                "url": "sqlite:///vortex.db",
                "echo": False,
                "pool_size": 5,
                "max_overflow": 10,
            },
            "llm": {
                "provider": "deepseek",
                "model": "deepseek-r1-70b",
                "temperature": 0.7,
                "max_tokens": 512,
                "api_key": None,
                "timeout_seconds": 10,
                "retry_attempts": 3,
            },
            "game": {
                "save_interval_minutes": 10,
                "max_history_length": 100,
                "default_guide": "thoth",
                "achievement_tracking_enabled": True,
            },
            "ui": {
                "prompt_symbol": "> ",
                "thinking_animation": True,
                "color_enabled": True,
                "text_speed": 0.01,  # seconds per character
            },
            "paths": {
                "saves": "saves",
                "logs": "logs",
                "assets": "assets",
            },
            "security": {
                "password_min_length": 8,
                "session_timeout_minutes": 30,
                "max_login_attempts": 5,
            },
        }
        
        self._type_definitions: Dict[str, ConfigType] = {
            "app.debug": ConfigType.BOOLEAN,
            "app.log_level": ConfigType.STRING,
            "database.url": ConfigType.STRING,
            "database.echo": ConfigType.BOOLEAN,
            "database.pool_size": ConfigType.INTEGER,
            "database.max_overflow": ConfigType.INTEGER,
            "llm.temperature": ConfigType.FLOAT,
            "llm.max_tokens": ConfigType.INTEGER,
            "llm.timeout_seconds": ConfigType.INTEGER,
            "llm.retry_attempts": ConfigType.INTEGER,
            "game.save_interval_minutes": ConfigType.INTEGER,
            "game.max_history_length": ConfigType.INTEGER,
            "ui.text_speed": ConfigType.FLOAT,
            "security.password_min_length": ConfigType.INTEGER,
            "security.session_timeout_minutes": ConfigType.INTEGER,
            "security.max_login_attempts": ConfigType.INTEGER,
        }
        
        self._validators: Dict[str, callable] = {
            "llm.temperature": lambda x: 0.0 <= x <= 1.0,
            "llm.max_tokens": lambda x: x > 0,
            "llm.timeout_seconds": lambda x: x > 0,
            "llm.retry_attempts": lambda x: x >= 0,
            "game.save_interval_minutes": lambda x: x >= 1,
            "game.max_history_length": lambda x: x > 0,
            "ui.text_speed": lambda x: x >= 0,
            "security.password_min_length": lambda x: x >= 6,
            "security.session_timeout_minutes": lambda x: x > 0,
            "security.max_login_attempts": lambda x: x > 0,
        }
        
        # Load environment variables
        self._load_from_env()
    
    def _load_from_env(self) -> None:
        """Load configuration values from environment variables."""
        prefix = "VORTEX_"
        
        for key in os.environ:
            if key.startswith(prefix):
                # Remove prefix and convert to lowercase
                config_key = key[len(prefix):].lower()
                
                # Replace double underscore with dot for category separation
                if "__" in config_key:
                    parts = config_key.split("__")
                    category = parts[0]
                    name = "__".join(parts[1:])
                    
                    # Ensure category exists
                    if category not in self._config:
                        self._config[category] = {}
                    
                    # Set the value with appropriate type conversion
                    env_value = os.environ[key]
                    full_key = f"{category}.{name}"
                    
                    try:
                        if full_key in self._type_definitions:
                            value = self._convert_value(env_value, self._type_definitions[full_key])
                        else:
                            # Try to detect the type
                            value = self._auto_convert_value(env_value)
                            
                        # Validate if we have a validator
                        if full_key in self._validators and not self._validators[full_key](value):
                            logger.warning(
                                f"Environment variable {key} value '{env_value}' failed validation. "
                                f"Using default value."
                            )
                            continue
                            
                        self._config[category][name] = value
                        logger.info(f"Loaded config from environment: {full_key}={value}")
                    except ValueError as e:
                        logger.warning(
                            f"Could not convert environment variable {key}={env_value}: {str(e)}"
                        )
    
    def _convert_value(self, value: str, type_def: ConfigType) -> Any:
        """Convert string value to the specified type.
        
        Args:
            value: String value to convert
            type_def: Target type for conversion
            
        Returns:
            Converted value of the appropriate type
            
        Raises:
            ValueError: If conversion fails
        """
        if type_def == ConfigType.BOOLEAN:
            return value.lower() in ("true", "yes", "1", "y", "on")
        elif type_def == ConfigType.INTEGER:
            return int(value)
        elif type_def == ConfigType.FLOAT:
            return float(value)
        elif type_def == ConfigType.LIST:
            return json.loads(value)
        elif type_def == ConfigType.DICT:
            return json.loads(value)
        else:  # STRING or unknown
            return value
    
    def _auto_convert_value(self, value: str) -> Any:
        """Attempt to automatically detect and convert value type.
        
        Args:
            value: String value to convert
            
        Returns:
            Value converted to the detected type
        """
        # Try boolean
        lower_value = value.lower()
        if lower_value in ("true", "false", "yes", "no", "y", "n", "1", "0", "on", "off"):
            return lower_value in ("true", "yes", "y", "1", "on")
            
        # Try integer
        try:
            if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
                return int(value)
        except ValueError:
            pass
            
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
            
        # Try JSON (list or dict)
        if (value.startswith("[") and value.endswith("]")) or (value.startswith("{") and value.endswith("}")):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
                
        # Default to string
        return value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key in format "category.name"
            default: Default value to return if key doesn't exist
            
        Returns:
            Configuration value or default
            
        Example:
            db_url = config.get("database.url")
            debug = config.get("app.debug", default=False)
        """
        if "." not in key:
            logger.warning(f"Invalid configuration key format: {key}")
            return default
            
        category, name = key.split(".", 1)
        
        if category not in self._config or name not in self._config[category]:
            return default
            
        return self._config[category][name]
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key in format "category.name"
            value: Value to set
            
        Raises:
            ConfigValidationError: If validation fails
            ValueError: If key format is invalid
            
        Example:
            config.set("database.url", "sqlite:///custom.db")
        """
        if "." not in key:
            raise ValueError(f"Invalid configuration key format: {key}")
            
        category, name = key.split(".", 1)
        
        # Create category if it doesn't exist
        if category not in self._config:
            self._config[category] = {}
            
        # Validate if we have a validator
        if key in self._validators and not self._validators[key](value):
            raise ConfigValidationError(f"Value {value} failed validation for {key}")
            
        # Set the value
        self._config[category][name] = value
    
    def has(self, key: str) -> bool:
        """Check if a configuration key exists.
        
        Args:
            key: Configuration key in format "category.name"
            
        Returns:
            True if the key exists, False otherwise
            
        Example:
            if config.has("llm.api_key"):
                # Use API key
        """
        if "." not in key:
            return False
            
        category, name = key.split(".", 1)
        return category in self._config and name in self._config[category]
    
    def get_all(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Get all configuration values, optionally filtered by category.
        
        Args:
            category: Optional category to filter by
            
        Returns:
            Dictionary of configuration values
            
        Example:
            all_db_config = config.get_all("database")
        """
        if category:
            return self._config.get(category, {}).copy()
        
        # Flatten the configuration for easier access
        result = {}
        for cat, values in self._config.items():
            for name, value in values.items():
                result[f"{cat}.{name}"] = value
                
        return result
    
    def load_from_file(self, file_path: Union[str, Path]) -> bool:
        """Load configuration from a JSON file.
        
        Args:
            file_path: Path to the JSON configuration file
            
        Returns:
            True if loaded successfully, False otherwise
            
        Example:
            config.load_from_file("config/production.json")
        """
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"Configuration file not found: {path}")
            return False
            
        try:
            with open(path, "r") as f:
                file_config = json.load(f)
                
            for category, values in file_config.items():
                if not isinstance(values, dict):
                    logger.warning(f"Invalid category format in config file: {category}")
                    continue
                    
                if category not in self._config:
                    self._config[category] = {}
                    
                for name, value in values.items():
                    key = f"{category}.{name}"
                    
                    # Validate if we have a validator
                    if key in self._validators and not self._validators[key](value):
                        logger.warning(
                            f"Value {value} for {key} in config file failed validation. "
                            f"Using existing value."
                        )
                        continue
                        
                    self._config[category][name] = value
                    
            logger.info(f"Loaded configuration from {path}")
            return True
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading configuration from {path}: {str(e)}")
            return False
    
    def save_to_file(self, file_path: Union[str, Path]) -> bool:
        """Save current configuration to a JSON file.
        
        Args:
            file_path: Path to save the configuration file
            
        Returns:
            True if saved successfully, False otherwise
            
        Example:
            config.save_to_file("config/current.json")
        """
        path = Path(file_path)
        
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path, "w") as f:
                json.dump(self._config, f, indent=2)
                
            logger.info(f"Saved configuration to {path}")
            return True
        except IOError as e:
            logger.error(f"Error saving configuration to {path}: {str(e)}")
            return False
    
    def reset_to_defaults(self, category: Optional[str] = None) -> None:
        """Reset configuration to default values.
        
        Args:
            category: Optional category to reset, or None for all
            
        Example:
            config.reset_to_defaults("database")  # Reset only database settings
            config.reset_to_defaults()  # Reset all settings
        """
        # Re-initialize with defaults
        new_instance = ConfigManager()
        
        if category:
            if category in self._config:
                self._config[category] = new_instance._config[category].copy()
        else:
            self._config = new_instance._config.copy()
            
        logger.info(f"Reset configuration to defaults: {category if category else 'all'}")


# Create a singleton instance
config = ConfigManager() 