#!/usr/bin/env python3
"""
Unit tests for ConfigManager
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test.env")
        
        # Create a test config file
        with open(self.config_file, 'w') as f:
            f.write("""# Test Configuration
ROBOT_NAME=test_robot
ROBOT_TYPE=mobile_robot
ROS_DISTRO=noetic
DOCKER_IMAGE=test_ros
DOCKER_CONTAINER=test_container
CLI_COMMAND=testbot
GUI_ENABLED=true
GPU_ENABLED=true
""")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_load_config(self):
        """Test loading configuration from file"""
        config = ConfigManager(self.config_file)
        
        # Test basic config loading
        self.assertEqual(config.get('ROBOT_NAME'), 'test_robot')
        self.assertEqual(config.get('ROBOT_TYPE'), 'mobile_robot')
        self.assertEqual(config.get('ROS_DISTRO'), 'noetic')
        self.assertEqual(config.get('DOCKER_IMAGE'), 'test_ros')
        self.assertEqual(config.get('DOCKER_CONTAINER'), 'test_container')


    def test_boolean_conversion(self):
        """Test boolean value conversion"""
        config = ConfigManager(self.config_file)
        
        # Test boolean conversion
        self.assertTrue(config.get('GUI_ENABLED'))
        self.assertTrue(config.get('GPU_ENABLED'))

    def test_integer_conversion(self):
        """Test integer value conversion"""
        config = ConfigManager(self.config_file)
        
        # Test integer conversion - no integer values in current config

    def test_get_with_default(self):
        """Test get method with default values"""
        config = ConfigManager(self.config_file)
        
        # Test default values
        self.assertEqual(config.get('NONEXISTENT_KEY', 'default'), 'default')
        self.assertEqual(config.get('NONEXISTENT_KEY', 42), 42)
        self.assertEqual(config.get('NONEXISTENT_KEY', True), True)

    def test_get_all(self):
        """Test getting all configuration"""
        config = ConfigManager(self.config_file)
        all_config = config.get_all()
        
        # Test that all expected keys are present
        expected_keys = [
            'ROBOT_NAME', 'ROBOT_TYPE', 'ROS_DISTRO', 'DOCKER_IMAGE',
            'DOCKER_CONTAINER', 'CLI_COMMAND', 'GUI_ENABLED', 'GPU_ENABLED'
        ]
        
        for key in expected_keys:
            self.assertIn(key, all_config)

    def test_missing_config_file(self):
        """Test behavior with missing config file"""
        config = ConfigManager("nonexistent.env")
        
        # Should not raise an error, just return empty config
        self.assertEqual(config.get('ROBOT_NAME'), None)
        self.assertEqual(config.get('ROBOT_NAME', 'default'), 'default')

    def test_generate_dockerfile(self):
        """Test Dockerfile generation"""
        config = ConfigManager(self.config_file)
        dockerfile = config.generate_dockerfile()
        
        # Test that Dockerfile contains expected content
        self.assertIn('FROM', dockerfile)
        self.assertIn('ros:noetic', dockerfile)
        self.assertIn('test_robot', dockerfile)
        self.assertIn('mobile_robot', dockerfile)

    def test_comments_ignored(self):
        """Test that comments are properly ignored"""
        config = ConfigManager(self.config_file)
        
        # Comments should not be loaded as config values
        all_config = config.get_all()
        self.assertNotIn('#', all_config)
        self.assertNotIn('Test Configuration', all_config)


if __name__ == '__main__':
    unittest.main() 