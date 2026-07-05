#!/usr/bin/env python3
"""
Tests for Configuration Module
"""

import pytest
import os
import tempfile
from src.utils.config import Config


@pytest.fixture
def temp_config():
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"tv_ip": "192.168.1.100", "passphrase": "ABC123"}')
        f.flush()
        yield f.name
    
    # Cleanup
    if os.path.exists(f.name):
        os.unlink(f.name)


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    
    assert config.get('fps') == 15
    assert config.get('quality') == 80
    assert config.get('port') == 9922
    assert config.get('websocket_port') == 8080


def test_config_load(temp_config):
    """Test loading configuration from file."""
    config = Config(temp_config)
    
    assert config.get('tv_ip') == '192.168.1.100'
    assert config.get('passphrase') == 'ABC123'
    # Defaults should still be present
    assert config.get('fps') == 15


def test_config_save_and_load():
    """Test saving and loading configuration."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_path = f.name
    
    try:
        # Create and modify config
        config = Config(config_path)
        config.set('tv_ip', '192.168.1.200')
        config.set('fps', 30)
        
        # Save
        assert config.save()
        
        # Load in new instance
        config2 = Config(config_path)
        assert config2.get('tv_ip') == '192.168.1.200'
        assert config2.get('fps') == 30
        
    finally:
        if os.path.exists(config_path):
            os.unlink(config_path)


def test_config_update():
    """Test updating multiple values at once."""
    config = Config()
    
    config.update({
        'fps': 20,
        'quality': 90,
        'tv_ip': '192.168.1.50'
    })
    
    assert config.get('fps') == 20
    assert config.get('quality') == 90
    assert config.get('tv_ip') == '192.168.1.50'


def test_config_reset():
    """Test resetting configuration to defaults."""
    config = Config()
    
    # Modify some values
    config.set('fps', 100)
    config.set('tv_ip', '1.2.3.4')
    
    # Reset
    config.reset()
    
    # Should be back to defaults
    assert config.get('fps') == 15
    assert config.get('tv_ip') == ''


def test_config_tv_list():
    """Test TV list management."""
    config = Config()
    
    # Add TVs
    config.add_tv({'ip': '192.168.1.100', 'name': 'Living Room'})
    config.add_tv({'ip': '192.168.1.101', 'name': 'Bedroom'})
    
    tv_list = config.get_tv_list()
    assert len(tv_list) == 2
    
    # Update existing TV
    config.add_tv({'ip': '192.168.1.100', 'name': 'Living Room TV'})
    tv_list = config.get_tv_list()
    assert len(tv_list) == 2
    assert tv_list[0]['name'] == 'Living Room TV'
    
    # Remove TV
    assert config.remove_tv('192.168.1.101')
    tv_list = config.get_tv_list()
    assert len(tv_list) == 1
    
    # Remove non-existent TV
    assert not config.remove_tv('192.168.1.999')
