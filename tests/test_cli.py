#!/usr/bin/env python3
"""
Integration tests for CLI functionality
"""

import unittest
import tempfile
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config_manager import ConfigManager
from utils.docker_manager import DockerManager


class TestCLI(unittest.TestCase):
    """Integration tests for CLI functionality"""

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
DOCKER_PORT=8080
HAS_CAMERA=true
HAS_LIDAR=false
MOTOR_COUNT=4
CLI_COMMAND=testbot
GUI_ENABLED=true
DEBUG_MODE=false
""")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_config_command(self):
        """Test config command functionality"""
        config = ConfigManager(self.config_file)
        
        # Test that all expected config values are present
        expected_config = {
            'ROBOT_NAME': 'test_robot',
            'ROBOT_TYPE': 'mobile_robot',
            'ROS_DISTRO': 'noetic',
            'DOCKER_IMAGE': 'test_ros',
            'DOCKER_CONTAINER': 'test_container',
            'DOCKER_PORT': 8080,
            'HAS_CAMERA': True,
            'HAS_LIDAR': False,
            'MOTOR_COUNT': 4,
            'CLI_COMMAND': 'testbot',
            'GUI_ENABLED': True,
            'DEBUG_MODE': False
        }
        
        for key, expected_value in expected_config.items():
            actual_value = config.get(key)
            self.assertEqual(actual_value, expected_value, 
                           f"Config key {key} mismatch: expected {expected_value}, got {actual_value}")

    @patch('subprocess.run')
    def test_build_command(self, mock_run):
        """Test build command functionality"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Successfully built image"
        
        config = ConfigManager(self.config_file)
        docker_mgr = DockerManager(config)
        
        # Test successful build
        result = docker_mgr.build_image("test.Dockerfile")
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_run_command(self, mock_run):
        """Test run command functionality"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Container started"
        
        config = ConfigManager(self.config_file)
        docker_mgr = DockerManager(config)
        
        # Test successful run
        result = docker_mgr.run_container()
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_stop_command(self, mock_run):
        """Test stop command functionality"""
        mock_run.return_value.returncode = 0
        
        config = ConfigManager(self.config_file)
        docker_mgr = DockerManager(config)
        
        # Test successful stop
        result = docker_mgr.stop_container()
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_status_command(self, mock_run):
        """Test status command functionality"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """[
            {
                "Names": ["test_container"],
                "State": "running",
                "Status": "Up 2 minutes",
                "Ports": "0.0.0.0:8080->8080/tcp",
                "Image": "test_ros:latest",
                "Created": "2023-01-01T00:00:00Z"
            }
        ]"""
        
        config = ConfigManager(self.config_file)
        docker_mgr = DockerManager(config)
        
        # Test status retrieval
        status = docker_mgr.get_container_status()
        self.assertIsInstance(status, dict)
        self.assertTrue(status.get('running', False))
        self.assertEqual(status.get('name'), 'test_container')

    @patch('subprocess.run')
    def test_logs_command(self, mock_run):
        """Test logs command functionality"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Container log output"
        
        config = ConfigManager(self.config_file)
        docker_mgr = DockerManager(config)
        
        # Test logs retrieval
        logs = docker_mgr.get_logs(lines=10)
        self.assertEqual(logs, "Container log output")
        mock_run.assert_called_once()

    def test_dockerfile_generation(self):
        """Test Dockerfile generation from config"""
        config = ConfigManager(self.config_file)
        dockerfile = config.generate_dockerfile()
        
        # Test that Dockerfile contains expected content
        self.assertIn('FROM', dockerfile)
        self.assertIn('ros:noetic', dockerfile)
        self.assertIn('test_robot', dockerfile)
        self.assertIn('mobile_robot', dockerfile)
        self.assertIn('test_ros', dockerfile)

    def test_config_validation(self):
        """Test configuration validation"""
        config = ConfigManager(self.config_file)
        
        # Test required fields
        required_fields = [
            'ROBOT_NAME', 'ROBOT_TYPE', 'ROS_DISTRO', 
            'DOCKER_IMAGE', 'DOCKER_CONTAINER', 'DOCKER_PORT'
        ]
        
        for field in required_fields:
            value = config.get(field)
            self.assertIsNotNone(value, f"Required field {field} is missing")
            self.assertNotEqual(value, "", f"Required field {field} is empty")

    def test_boolean_config_handling(self):
        """Test boolean configuration handling"""
        config = ConfigManager(self.config_file)
        
        # Test boolean fields
        boolean_fields = {
            'HAS_CAMERA': True,
            'HAS_LIDAR': False,
            'GUI_ENABLED': True,
            'DEBUG_MODE': False
        }
        
        for field, expected_value in boolean_fields.items():
            actual_value = config.get(field)
            self.assertEqual(actual_value, expected_value, 
                           f"Boolean field {field} mismatch")

    def test_integer_config_handling(self):
        """Test integer configuration handling"""
        config = ConfigManager(self.config_file)
        
        # Test integer fields
        integer_fields = {
            'MOTOR_COUNT': 4,
            'DOCKER_PORT': 8080
        }
        
        for field, expected_value in integer_fields.items():
            actual_value = config.get(field)
            self.assertEqual(actual_value, expected_value, 
                           f"Integer field {field} mismatch")

    def test_cli_command_config(self):
        """Test CLI command configuration"""
        config = ConfigManager(self.config_file)
        
        # Test CLI command configuration
        cli_command = config.get('CLI_COMMAND')
        self.assertEqual(cli_command, 'testbot')
        
        # Test that it's a valid command name
        self.assertIsInstance(cli_command, str)
        self.assertGreater(len(cli_command), 0)
        self.assertTrue(cli_command.isalnum() or '_' in cli_command)

    def test_docker_config_integration(self):
        """Test Docker configuration integration"""
        config = ConfigManager(self.config_file)
        docker_mgr = DockerManager(config)
        
        # Test that Docker manager has access to config
        self.assertIsNotNone(docker_mgr.docker_config)
        self.assertEqual(docker_mgr.docker_config.get('DOCKER_IMAGE'), 'test_ros')
        self.assertEqual(docker_mgr.docker_config.get('DOCKER_CONTAINER'), 'test_container')
        self.assertEqual(docker_mgr.docker_config.get('DOCKER_PORT'), 8080)


if __name__ == '__main__':
    unittest.main() 