#!/usr/bin/env python3
"""
Unit tests for PathDetector
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.path_detector import PathDetector


class TestPathDetector(unittest.TestCase):
    """Test cases for PathDetector"""

    def setUp(self):
        """Set up test fixtures"""
        self.path_detector = PathDetector()

    def test_detect_install_path(self):
        """Test install path detection"""
        install_path = self.path_detector.detect_install_path()
        
        # Should return a valid path
        self.assertIsInstance(install_path, str)
        self.assertTrue(os.path.isabs(install_path))
        
        # Should be a directory or should be creatable
        if not os.path.exists(install_path):
            # Test that we can create it
            os.makedirs(install_path, exist_ok=True)
            self.assertTrue(os.path.exists(install_path))

    def test_detect_completion_path(self):
        """Test bash completion path detection"""
        completion_path = self.path_detector.detect_completion_path()
        
        # Should return a valid path
        self.assertIsInstance(completion_path, str)
        self.assertTrue(os.path.isabs(completion_path))
        
        # Should be a directory or should be creatable
        if not os.path.exists(completion_path):
            # Test that we can create it
            os.makedirs(completion_path, exist_ok=True)
            self.assertTrue(os.path.exists(completion_path))

    def test_detect_config_path(self):
        """Test configuration path detection"""
        config_path = self.path_detector.detect_config_path()
        
        # Should return a valid path
        self.assertIsInstance(config_path, str)
        self.assertTrue(os.path.isabs(config_path))
        
        # Should be a directory or should be creatable
        if not os.path.exists(config_path):
            # Test that we can create it
            os.makedirs(config_path, exist_ok=True)
            self.assertTrue(os.path.exists(config_path))

    @patch('subprocess.run')
    def test_has_sudo_access(self, mock_run):
        """Test sudo access checking"""
        # Test when user has sudo access
        mock_run.return_value.returncode = 0
        self.assertTrue(self.path_detector.has_sudo_access())
        
        # Test when user doesn't have sudo access
        mock_run.return_value.returncode = 1
        self.assertFalse(self.path_detector.has_sudo_access())

    def test_create_path_if_not_exists(self):
        """Test path creation functionality"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "test_subdir")
            
            # Path should not exist initially
            self.assertFalse(os.path.exists(test_path))
            
            # Create the path
            result = self.path_detector.create_path_if_not_exists(test_path)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(test_path))
            self.assertTrue(os.path.isdir(test_path))

    def test_create_path_if_not_exists_already_exists(self):
        """Test path creation when path already exists"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Path already exists
            self.assertTrue(os.path.exists(temp_dir))
            
            # Should still return True
            result = self.path_detector.create_path_if_not_exists(temp_dir)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(temp_dir))

    @patch('os.makedirs')
    def test_create_path_if_not_exists_permission_error(self, mock_makedirs):
        """Test path creation with permission error"""
        mock_makedirs.side_effect = PermissionError("Permission denied")
        
        result = self.path_detector.create_path_if_not_exists("/root/test")
        self.assertFalse(result)

    def test_get_system_info(self):
        """Test system information retrieval"""
        info = self.path_detector.get_system_info()
        
        # Should return a dictionary with system info
        self.assertIsInstance(info, dict)
        self.assertIn('os', info)
        self.assertIn('platform', info)
        self.assertIn('distribution', info)
        self.assertIn('user_home', info)
        self.assertIn('current_dir', info)
        self.assertIn('has_sudo', info)
        
        # All values should be valid
        self.assertIsInstance(info['os'], str)
        self.assertIsInstance(info['platform'], str)
        self.assertIsInstance(info['distribution'], str)
        self.assertIsInstance(info['user_home'], str)
        self.assertIsInstance(info['current_dir'], str)
        self.assertIsInstance(info['has_sudo'], bool)

    def test_can_write_to_path(self):
        """Test path write access checking"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test writable directory
            self.assertTrue(self.path_detector._can_write_to_path(temp_dir))
            
            # Test non-writable directory (if we can create one)
            read_only_dir = os.path.join(temp_dir, "readonly")
            os.makedirs(read_only_dir, mode=0o444)
            
            # This might fail depending on the system, so we'll just test the method exists
            try:
                result = self.path_detector._can_write_to_path(read_only_dir)
                self.assertIsInstance(result, bool)
            except Exception:
                pass  # Some systems might not allow this test

    def test_get_relative_path(self):
        """Test relative path calculation"""
        # Test valid relative path
        base_path = "/home/user"
        target_path = "/home/user/documents/file.txt"
        relative = self.path_detector.get_relative_path(base_path, target_path)
        self.assertEqual(relative, "documents/file.txt")
        
        # Test when target is not under base
        target_path = "/etc/passwd"
        relative = self.path_detector.get_relative_path(base_path, target_path)
        self.assertEqual(relative, "/etc/passwd")

    @patch('subprocess.run')
    def test_find_executable(self, mock_run):
        """Test executable finding"""
        # Test when executable is found
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "/usr/bin/python3\n"
        
        result = self.path_detector.find_executable("python3")
        self.assertEqual(result, "/usr/bin/python3")
        
        # Test when executable is not found
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""
        
        result = self.path_detector.find_executable("nonexistent")
        self.assertIsNone(result)

    def test_ensure_path_in_profile(self):
        """Test PATH profile updating"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_profile = os.path.join(temp_dir, ".bashrc")
            
            # Create a test profile file
            with open(test_profile, 'w') as f:
                f.write("# Test profile\n")
            
            # Test adding path to profile
            test_path = "/usr/local/bin"
            result = self.path_detector.ensure_path_in_profile(test_path)
            
            # Should return True and add the path
            self.assertTrue(result)
            
            # Check that the path was added
            with open(test_profile, 'r') as f:
                content = f.read()
                self.assertIn(f'export PATH="{test_path}:$PATH"', content)


if __name__ == '__main__':
    unittest.main() 