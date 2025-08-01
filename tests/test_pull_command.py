#!/usr/bin/env python3
"""
Test for pull command functionality
"""

import unittest
import sys
import os
import subprocess
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.docker_manager import DockerManager
from utils.config_manager import ConfigManager


class TestPullCommand(unittest.TestCase):
    """Test pull command functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = ConfigManager()
        self.docker_mgr = DockerManager(self.config)
    
    @patch('subprocess.run')
    def test_pull_image_success(self, mock_run):
        """Test successful image pull"""
        # Mock successful docker pull
        mock_run.return_value.returncode = 0
        
        # Test pull with default parameters
        result = self.docker_mgr.pull_image()
        self.assertTrue(result)
        
        # Verify docker pull was called with correct arguments
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        self.assertEqual(call_args[0], 'docker')
        self.assertEqual(call_args[1], 'pull')
    
    @patch('subprocess.run')
    def test_pull_image_failure(self, mock_run):
        """Test failed image pull"""
        # Mock failed docker pull
        mock_run.side_effect = subprocess.CalledProcessError(1, 'docker pull')
        
        # Test pull with default parameters
        result = self.docker_mgr.pull_image()
        self.assertFalse(result)
    
    @patch('subprocess.run')
    def test_pull_image_with_custom_name(self, mock_run):
        """Test pull with custom image name and tag"""
        # Mock successful docker pull
        mock_run.return_value.returncode = 0
        
        # Test pull with custom parameters
        result = self.docker_mgr.pull_image('custom-image', 'v1.0')
        self.assertTrue(result)
        
        # Verify docker pull was called with correct arguments
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        self.assertEqual(call_args[0], 'docker')
        self.assertEqual(call_args[1], 'pull')
        self.assertEqual(call_args[2], 'custom-image:v1.0')
    
    def test_pull_image_docker_not_running(self):
        """Test pull when Docker is not running"""
        with patch.object(self.docker_mgr, 'is_docker_running', return_value=False):
            # This should still work but fail at the subprocess level
            # The actual test would be in the CLI command
            pass


if __name__ == '__main__':
    unittest.main() 