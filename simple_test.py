#!/usr/bin/env python3
"""
Simple Test Script for Robot Platform Environment
Tests core features without external dependencies
"""

import os
import sys
import subprocess
import time

class SimpleRobotPlatformTester:
    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.cli_command = None
        
    def log(self, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def test_passed(self, test_name, details=""):
        self.results['passed'].append(test_name)
        self.log(f"✅ {test_name} - PASSED", "PASS")
        if details:
            self.log(f"   Details: {details}", "INFO")
            
    def test_failed(self, test_name, error=""):
        self.results['failed'].append(test_name)
        self.log(f"❌ {test_name} - FAILED", "FAIL")
        if error:
            self.log(f"   Error: {error}", "ERROR")
            
    def test_warning(self, test_name, warning=""):
        self.results['warnings'].append(test_name)
        self.log(f"⚠️  {test_name} - WARNING", "WARN")
        if warning:
            self.log(f"   Warning: {warning}", "WARN")
    
    def run_command(self, command, capture_output=True):
        """Run a command and return result"""
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                return result.returncode == 0, result.stdout, result.stderr
            else:
                result = subprocess.run(command, shell=True, timeout=30)
                return result.returncode == 0, "", ""
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def test_1_environment_check(self):
        """Test 1: Check current environment"""
        self.log("Testing environment...", "TEST")
        
        # Check current directory
        cwd = os.getcwd()
        self.log(f"Current directory: {cwd}", "INFO")
        
        # Check if we're in the right place
        if "robot_platform_env" in cwd or os.path.exists("rpe"):
            self.test_passed("Environment", "In robot platform environment directory")
        else:
            self.test_warning("Environment", "May not be in robot platform environment directory")
    
    def test_2_file_structure(self):
        """Test 2: Check if all required files exist"""
        self.log("Testing file structure...", "TEST")
        
        required_files = [
            'rpe',
            'rpe-webgui.py', 
            'install.sh',
            'platform.env',
            'platform.env.example',
            'requirements.txt',
            'README.md',
            'PROJECT_SUMMARY.md'
        ]
        
        required_dirs = [
            'src/utils',
            'web',
            'templates',
            'tests',
            'scripts',
            'completion'
        ]
        
        missing_files = []
        missing_dirs = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
                
        for dir_path in required_dirs:
            if not os.path.isdir(dir_path):
                missing_dirs.append(dir_path)
        
        if not missing_files and not missing_dirs:
            self.test_passed("File Structure", f"All {len(required_files)} files and {len(required_dirs)} directories present")
        else:
            self.test_failed("File Structure", f"Missing: {missing_files + missing_dirs}")
    
    def test_3_cli_installation(self):
        """Test 3: Check CLI command installation"""
        self.log("Testing CLI installation...", "TEST")
        
        # Check if rpe command is available
        success, stdout, stderr = self.run_command("which rpe")
        if success and stdout.strip():
            self.cli_command = "rpe"
            self.test_passed("CLI Installation - rpe", f"Found at: {stdout.strip()}")
        else:
            # Check for autobot command
            success, stdout, stderr = self.run_command("which autobot")
            if success and stdout.strip():
                self.cli_command = "autobot"
                self.test_passed("CLI Installation - autobot", f"Found at: {stdout.strip()}")
            else:
                # Check if rpe script exists locally
                if os.path.exists("./rpe") and os.access("./rpe", os.X_OK):
                    self.cli_command = "./rpe"
                    self.test_passed("CLI Installation - local rpe", "Local rpe script is executable")
                else:
                    self.test_failed("CLI Installation", "Neither 'rpe' nor 'autobot' command found")
    
    def test_4_cli_help(self):
        """Test 4: Check CLI help command"""
        self.log("Testing CLI help...", "TEST")
        
        if not self.cli_command:
            self.test_failed("CLI Help", "No CLI command available")
            return
            
        success, stdout, stderr = self.run_command(f"{self.cli_command} --help")
        if success and "usage:" in stdout:
            self.test_passed("CLI Help", "Help command works correctly")
        else:
            self.test_failed("CLI Help", f"Help command failed: {stderr}")
    
    def test_5_cli_config(self):
        """Test 5: Check CLI config command"""
        self.log("Testing CLI config...", "TEST")
        
        if not self.cli_command:
            self.test_failed("CLI Config", "No CLI command available")
            return
            
        success, stdout, stderr = self.run_command(f"{self.cli_command} config")
        if success and "ROBOT_NAME:" in stdout:
            self.test_passed("CLI Config", "Config command works correctly")
        else:
            self.test_failed("CLI Config", f"Config command failed: {stderr}")
    
    def test_6_cli_status(self):
        """Test 6: Check CLI status command"""
        self.log("Testing CLI status...", "TEST")
        
        if not self.cli_command:
            self.test_failed("CLI Status", "No CLI command available")
            return
            
        success, stdout, stderr = self.run_command(f"{self.cli_command} status")
        if success:
            self.test_passed("CLI Status", "Status command works correctly")
        else:
            self.test_warning("CLI Status", f"Status command failed: {stderr}")
    
    def test_7_python_modules(self):
        """Test 7: Check Python modules"""
        self.log("Testing Python modules...", "TEST")
        
        try:
            sys.path.insert(0, 'src')
            from utils.config_manager import ConfigManager
            from utils.docker_manager import DockerManager
            from utils.path_detector import PathDetector
            self.test_passed("Python Modules", "All utility modules import correctly")
        except ImportError as e:
            self.test_failed("Python Modules", f"Import error: {e}")
    
    def test_8_web_dependencies(self):
        """Test 8: Check web dependencies"""
        self.log("Testing web dependencies...", "TEST")
        
        if not os.path.exists('web/package.json'):
            self.test_failed("Web Dependencies", "package.json not found")
            return
            
        success, stdout, stderr = self.run_command("cd web && npm list --depth=0")
        if success:
            self.test_passed("Web Dependencies", "Node.js dependencies installed")
        else:
            self.test_failed("Web Dependencies", f"npm list failed: {stderr}")
    
    def test_9_webgui_script(self):
        """Test 9: Check webgui script"""
        self.log("Testing webgui script...", "TEST")
        
        if not os.path.exists('rpe-webgui.py'):
            self.test_failed("WebGUI Script", "rpe-webgui.py not found")
            return
            
        # Check if script is executable
        if os.access('rpe-webgui.py', os.X_OK):
            self.test_passed("WebGUI Script", "rpe-webgui.py is executable")
        else:
            self.test_warning("WebGUI Script", "rpe-webgui.py is not executable")
    
    def test_10_installation_script(self):
        """Test 10: Check installation script"""
        self.log("Testing installation script...", "TEST")
        
        if not os.path.exists('install.sh'):
            self.test_failed("Installation Script", "install.sh not found")
            return
            
        if os.access('install.sh', os.X_OK):
            self.test_passed("Installation Script", "install.sh is executable")
        else:
            self.test_warning("Installation Script", "install.sh is not executable")
    
    def test_11_configuration_file(self):
        """Test 11: Check configuration file"""
        self.log("Testing configuration file...", "TEST")
        
        if not os.path.exists('platform.env'):
            self.test_failed("Configuration File", "platform.env not found")
            return
            
        try:
            with open('platform.env', 'r') as f:
                content = f.read()
                if 'ROBOT_NAME=' in content and 'ROS_DISTRO=' in content:
                    self.test_passed("Configuration File", "platform.env contains required settings")
                else:
                    self.test_warning("Configuration File", "platform.env may be missing some settings")
        except Exception as e:
            self.test_failed("Configuration File", f"Cannot read platform.env: {e}")
    
    def test_12_bash_completion(self):
        """Test 12: Check bash completion"""
        self.log("Testing bash completion...", "TEST")
        
        if not os.path.exists('completion/rpe'):
            self.test_warning("Bash Completion", "completion/rpe not found")
        else:
            self.test_passed("Bash Completion", "Bash completion script exists")
    
    def test_13_test_suite(self):
        """Test 13: Check test suite"""
        self.log("Testing test suite...", "TEST")
        
        if not os.path.exists('tests/run_tests.py'):
            self.test_warning("Test Suite", "tests/run_tests.py not found")
            return
            
        success, stdout, stderr = self.run_command("python3 tests/run_tests.py --help", capture_output=False)
        if success:
            self.test_passed("Test Suite", "Test suite is runnable")
        else:
            self.test_warning("Test Suite", "Test suite may have issues")
    
    def test_14_docker_integration(self):
        """Test 14: Check Docker integration"""
        self.log("Testing Docker integration...", "TEST")
        
        success, stdout, stderr = self.run_command("docker --version")
        if success:
            self.test_passed("Docker Installation", f"Docker available: {stdout.strip()}")
        else:
            self.test_failed("Docker Installation", "Docker not available")
            return
            
        success, stdout, stderr = self.run_command("docker ps")
        if success:
            self.test_passed("Docker Access", "Docker daemon accessible")
        else:
            self.test_failed("Docker Access", "Cannot access Docker daemon")
    
    def test_15_web_server_check(self):
        """Test 15: Check if web server is running"""
        self.log("Testing web server...", "TEST")
        
        # Try to check if port 3000 is in use
        success, stdout, stderr = self.run_command("lsof -i :3000")
        if success and stdout.strip():
            self.test_passed("Web Server", "Web server appears to be running on port 3000")
        else:
            self.test_warning("Web Server", "No web server detected on port 3000")
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("🤖 Starting Robot Platform Environment Test Suite", "HEADER")
        self.log("=" * 60, "HEADER")
        
        tests = [
            self.test_1_environment_check,
            self.test_2_file_structure,
            self.test_3_cli_installation,
            self.test_4_cli_help,
            self.test_5_cli_config,
            self.test_6_cli_status,
            self.test_7_python_modules,
            self.test_8_web_dependencies,
            self.test_9_webgui_script,
            self.test_10_installation_script,
            self.test_11_configuration_file,
            self.test_12_bash_completion,
            self.test_13_test_suite,
            self.test_14_docker_integration,
            self.test_15_web_server_check
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.test_failed(test.__name__, f"Test crashed: {e}")
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        self.log("=" * 60, "HEADER")
        self.log("📊 TEST SUMMARY", "HEADER")
        self.log("=" * 60, "HEADER")
        
        total_tests = len(self.results['passed']) + len(self.results['failed']) + len(self.results['warnings'])
        
        self.log(f"Total Tests: {total_tests}", "SUMMARY")
        self.log(f"✅ Passed: {len(self.results['passed'])}", "SUMMARY")
        self.log(f"❌ Failed: {len(self.results['failed'])}", "SUMMARY")
        self.log(f"⚠️  Warnings: {len(self.results['warnings'])}", "SUMMARY")
        
        if self.results['failed']:
            self.log("\n❌ FAILED TESTS:", "SUMMARY")
            for test in self.results['failed']:
                self.log(f"   - {test}", "SUMMARY")
        
        if self.results['warnings']:
            self.log("\n⚠️  WARNINGS:", "SUMMARY")
            for test in self.results['warnings']:
                self.log(f"   - {test}", "SUMMARY")
        
        if not self.results['failed']:
            self.log("\n🎉 All critical tests passed! Robot Platform Environment is working correctly.", "SUCCESS")
        else:
            self.log("\n🔧 Some issues detected. Please review the failed tests above.", "WARNING")

if __name__ == "__main__":
    tester = SimpleRobotPlatformTester()
    tester.run_all_tests()