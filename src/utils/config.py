#!/usr/bin/env python3
"""
Configuration Module

Handles application configuration and settings.
"""

import json
import logging
import os
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """
    Manages application configuration.
    
    Configuration is stored in a JSON file and can be loaded/saved.
    """
    
    DEFAULT_CONFIG = {
        'tv_ip': '',
        'passphrase': '',
        'fps': 15,
        'quality': 80,
        'port': 9922,
        'websocket_port': 8080,
        'last_tv': None,
        'auto_connect': False
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration.
        
        Args:
            config_path: Path to config file (default: ~/.mirror_screen_lg/config.json).
        """
        if config_path is None:
            config_dir = Path.home() / '.mirror_screen_lg'
            config_dir.mkdir(exist_ok=True)
            self.config_path = config_dir / 'config.json'
        else:
            self.config_path = Path(config_path)
        
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self.load()
        logger.info(f"Config initialized (Path: {self.config_path})")
    
    def load(self) -> bool:
        """
        Load configuration from file.
        
        Returns:
            bool: True if loaded successfully, False otherwise.
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    for key, value in self.DEFAULT_CONFIG.items():
                        if key not in loaded_config:
                            loaded_config[key] = value
                    self.config = loaded_config
                logger.info(f"Config loaded from {self.config_path}")
                return True
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
        
        return False
    
    def save(self) -> bool:
        """
        Save configuration to file.
        
        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Config saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key.
            default: Default value if key not found.
            
        Returns:
            Any: Configuration value.
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key.
            value: Value to set.
        """
        if key in self.DEFAULT_CONFIG or key in self.config:
            self.config[key] = value
            logger.debug(f"Config set: {key} = {value}")
        else:
            logger.warning(f"Unknown config key: {key}")
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple configuration values.
        
        Args:
            updates: Dictionary of key-value pairs to update.
        """
        for key, value in updates.items():
            self.set(key, value)
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        logger.info("Config reset to defaults")
    
    def get_tv_list(self) -> list:
        """
        Get the list of saved TVs.
        
        Returns:
            list: List of TV configurations.
        """
        return self.config.get('tv_list', [])
    
    def add_tv(self, tv_config: Dict[str, Any]) -> None:
        """
        Add a TV configuration to the list.
        
        Args:
            tv_config: TV configuration dictionary.
        """
        if 'tv_list' not in self.config:
            self.config['tv_list'] = []
        
        # Check if TV already exists
        for i, tv in enumerate(self.config['tv_list']):
            if tv.get('ip') == tv_config.get('ip'):
                self.config['tv_list'][i] = tv_config
                logger.info(f"Updated TV: {tv_config.get('ip')}")
                return
        
        # Add new TV
        self.config['tv_list'].append(tv_config)
        logger.info(f"Added TV: {tv_config.get('ip')}")
    
    def remove_tv(self, tv_ip: str) -> bool:
        """
        Remove a TV configuration from the list.
        
        Args:
            tv_ip: IP address of the TV to remove.
            
        Returns:
            bool: True if TV was removed, False otherwise.
        """
        if 'tv_list' not in self.config:
            return False
        
        for i, tv in enumerate(self.config['tv_list']):
            if tv.get('ip') == tv_ip:
                del self.config['tv_list'][i]
                logger.info(f"Removed TV: {tv_ip}")
                return True
        
        return False
