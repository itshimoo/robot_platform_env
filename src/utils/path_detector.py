#!/usr/bin/env python3
"""
Path Detector for RobotLab
Provides dynamic path detection for cross-platform compatibility
"""

import os
import subprocess
from pathlib import Path
from typing import Optional


class PathDetector:
    """Detects and manages installation paths across different systems"""
    
    def __init__(self):
        """Initialize the path detector"""
        self.user_home = os.path.expanduser("~")
        self.current_dir = os.getcwd()
    
    def detect_install_path(self) -> str:
        """Detect the best installation path for binaries"""
        # Try system-wide installation first
        system_paths = [
            "/usr/local/bin",
            "/usr/bin",
            "/opt/robotlab/bin"
        ]
        
        for path in system_paths:
            if self._can_write_to_path(path):
                return path
        
        # Fallback to user-specific path
        user_bin = os.path.join(self.user_home, ".local/bin")
        if not os.path.exists(user_bin):
            os.makedirs(user_bin, exist_ok=True)
        return user_bin
    
    def detect_completion_path(self) -> str:
        """Detect bash completion directory"""
        # Try system-wide completion directory
        system_completion_paths = [
            "/etc/bash_completion.d",
            "/usr/share/bash-completion/completions",
            "/usr/local/etc/bash_completion.d"
        ]
        
        for path in system_completion_paths:
            if self._can_write_to_path(path):
                return path
        
        # Fallback to user-specific path
        user_completion = os.path.join(self.user_home, ".bash_completion.d")
        if not os.path.exists(user_completion):
            os.makedirs(user_completion, exist_ok=True)
        return user_completion
    
    def detect_config_path(self) -> str:
        """Detect configuration directory"""
        # Try system-wide config directory
        system_config_paths = [
            "/etc/robotlab",
            "/usr/local/etc/robotlab",
            "/opt/robotlab/config"
        ]
        
        for path in system_config_paths:
            if self._can_write_to_path(path):
                return path
        
        # Fallback to user-specific path
        user_config = os.path.join(self.user_home, ".config/robotlab")
        if not os.path.exists(user_config):
            os.makedirs(user_config, exist_ok=True)
        return user_config
    
    def _can_write_to_path(self, path: str) -> bool:
        """Check if we can write to a given path"""
        try:
            if not os.path.exists(path):
                # Try to create the directory
                os.makedirs(path, exist_ok=True)
            
            # Test write access
            test_file = os.path.join(path, ".test_write")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            return True
        except (OSError, PermissionError):
            return False
    
    def has_sudo_access(self) -> bool:
        """Check if user has sudo access"""
        try:
            result = subprocess.run(
                ['sudo', '-n', 'true'], 
                capture_output=True, 
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_system_info(self) -> dict:
        """Get system information for path detection"""
        info = {
            'os': os.name,
            'platform': os.uname().sysname if hasattr(os, 'uname') else 'unknown',
            'distribution': self._detect_distribution(),
            'user_home': self.user_home,
            'current_dir': self.current_dir,
            'has_sudo': self.has_sudo_access()
        }
        return info
    
    def _detect_distribution(self) -> str:
        """Detect Linux distribution"""
        try:
            # Try to read distribution info
            dist_files = [
                '/etc/os-release',
                '/etc/lsb-release',
                '/etc/redhat-release',
                '/etc/debian_version'
            ]
            
            for dist_file in dist_files:
                if os.path.exists(dist_file):
                    with open(dist_file, 'r') as f:
                        content = f.read().lower()
                        if 'ubuntu' in content:
                            return 'ubuntu'
                        elif 'debian' in content:
                            return 'debian'
                        elif 'centos' in content or 'redhat' in content:
                            return 'redhat'
                        elif 'fedora' in content:
                            return 'fedora'
                        elif 'arch' in content:
                            return 'arch'
            
            return 'unknown'
        except Exception:
            return 'unknown'
    
    def create_path_if_not_exists(self, path: str) -> bool:
        """Create path if it doesn't exist"""
        try:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                print(f"Created directory: {path}")
            return True
        except Exception as e:
            print(f"Error creating path {path}: {e}")
            return False
    
    def get_relative_path(self, base_path: str, target_path: str) -> str:
        """Get relative path from base to target"""
        try:
            base = Path(base_path).resolve()
            target = Path(target_path).resolve()
            return str(target.relative_to(base))
        except ValueError:
            return target_path
    
    def find_executable(self, name: str) -> Optional[str]:
        """Find executable in PATH"""
        try:
            result = subprocess.run(
                ['which', name], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None
    
    def ensure_path_in_profile(self, path: str) -> bool:
        """Ensure path is in user's PATH environment"""
        profile_files = [
            os.path.join(self.user_home, '.bashrc'),
            os.path.join(self.user_home, '.bash_profile'),
            os.path.join(self.user_home, '.profile')
        ]
        
        path_export = f'export PATH="{path}:$PATH"'
        
        for profile_file in profile_files:
            if os.path.exists(profile_file):
                try:
                    with open(profile_file, 'r') as f:
                        content = f.read()
                    
                    if path_export not in content:
                        with open(profile_file, 'a') as f:
                            f.write(f'\n# RobotLab PATH\n{path_export}\n')
                        print(f"Added PATH to {profile_file}")
                        return True
                except Exception as e:
                    print(f"Error updating {profile_file}: {e}")
        
        return False


def main():
    """Test the path detector"""
    detector = PathDetector()
    
    print("System Information:")
    info = detector.get_system_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print(f"\nInstall Path: {detector.detect_install_path()}")
    print(f"Completion Path: {detector.detect_completion_path()}")
    print(f"Config Path: {detector.detect_config_path()}")
    print(f"Has Sudo Access: {detector.has_sudo_access()}")


if __name__ == "__main__":
    main() 