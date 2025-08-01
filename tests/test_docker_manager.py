#!/usr/bin/env python3
"""
Unit tests for DockerManager
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.docker_manager import DockerManager
from utils.config_manager import ConfigManager


class TestDockerManager(unittest.TestCase):
    """Test cases for DockerManager"""

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

CLI_COMMAND=testbot
GUI_ENABLED=true
DEBUG_MODE=false
""")
        
        self.config = ConfigManager(self.config_file)
        self.docker_mgr = DockerManager(self.config)

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    @patch('subprocess.run')
    def test_is_docker_running(self, mock_run):
        """Test Docker daemon status check"""
        # Test when Docker is running
        mock_run.return_value.returncode = 0
        self.assertTrue(self.docker_mgr.is_docker_running())
        
        # Test when Docker is not running
        mock_run.return_value.returncode = 1
        self.assertFalse(self.docker_mgr.is_docker_running())

    @patch('subprocess.run')
    def test_build_image_success(self, mock_run):
        """Test successful Docker image build"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Successfully built image"
        
        result = self.docker_mgr.build_image("test.Dockerfile")
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_build_image_failure(self, mock_run):
        """Test failed Docker image build"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Build failed"
        
        result = self.docker_mgr.build_image("test.Dockerfile")
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_run_container_success(self, mock_run):
        """Test successful container run"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Container started"
        
        result = self.docker_mgr.run_container()
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_run_container_failure(self, mock_run):
        """Test failed container run"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Failed to start container"
        
        result = self.docker_mgr.run_container()
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_stop_container_success(self, mock_run):
        """Test successful container stop"""
        mock_run.return_value.returncode = 0
        
        result = self.docker_mgr.stop_container()
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_stop_container_failure(self, mock_run):
        """Test failed container stop"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Failed to stop container"
        
        result = self.docker_mgr.stop_container()
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_get_container_status(self, mock_run):
        """Test container status retrieval"""
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
        
        status = self.docker_mgr.get_container_status()
        
        self.assertIsInstance(status, dict)
        self.assertTrue(status.get('running', False))
        self.assertEqual(status.get('name'), 'test_container')
        self.assertEqual(status.get('status'), 'Up 2 minutes')

    @patch('subprocess.run')
    def test_get_container_status_not_running(self, mock_run):
        """Test container status when not running"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "[]"  # No containers running
        
        status = self.docker_mgr.get_container_status()
        
        self.assertIsInstance(status, dict)
        self.assertFalse(status.get('running', True))
        self.assertIsNone(status.get('name'))

    @patch('subprocess.run')
    def test_get_logs(self, mock_run):
        """Test container logs retrieval"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Container log output"
        
        logs = self.docker_mgr.get_logs(lines=10)
        self.assertEqual(logs, "Container log output")
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_get_logs_failure(self, mock_run):
        """Test container logs retrieval failure"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Failed to get logs"
        
        logs = self.docker_mgr.get_logs(lines=10)
        self.assertIn("Error getting logs", logs)

    @patch('subprocess.Popen')
    def test_shell_into_container_success(self, mock_popen):
        """Test successful shell into container"""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        mock_process.wait.return_value = 0
        
        result = self.docker_mgr.shell_into_container()
        self.assertTrue(result)
        mock_popen.assert_called_once()

    @patch('subprocess.Popen')
    def test_shell_into_container_failure(self, mock_popen):
        """Test failed shell into container"""
        mock_popen.side_effect = Exception("Docker not available")
        
        result = self.docker_mgr.shell_into_container()
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_list_images(self, mock_run):
        """Test Docker images listing"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """[
            {
                "Repository": "test_ros",
                "Tag": "latest",
                "ImageID": "abc123",
                "CreatedAt": "2023-01-01T00:00:00Z",
                "Size": "1.2GB"
            }
        ]"""
        
        images = self.docker_mgr.list_images()
        
        self.assertIsInstance(images, list)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]['Repository'], 'test_ros')
        self.assertEqual(images[0]['Tag'], 'latest')

    @patch('subprocess.run')
    def test_cleanup_images(self, mock_run):
        """Test Docker images cleanup"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Cleaned up 5 images"
        
        result = self.docker_mgr.cleanup_images()
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_cleanup_images_failure(self, mock_run):
        """Test Docker images cleanup failure"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Failed to cleanup images"
        
        result = self.docker_mgr.cleanup_images()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main() 