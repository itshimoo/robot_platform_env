#!/usr/bin/env python3
"""
Robot Platform Environment Web GUI CLI
Starts the Node.js web server for the Robot Platform Environment GUI
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# Add the src directory to Python path for imports
current_dir = Path(__file__).parent
# Since we're in web/, go up one level to find src/
project_dir = current_dir.parent
src_dir = project_dir / "src"
sys.path.insert(0, str(src_dir))

from utils.config_manager import ConfigManager


def check_nodejs():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_npm():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_dependencies():
    """Install Node.js dependencies"""
    # current_dir is already the web directory
    package_json = current_dir / "package.json"
    
    if not package_json.exists():
        print("❌ package.json not found in web directory")
        return False
    
    print("Installing Node.js dependencies...")
    try:
        subprocess.run(['npm', 'install'], cwd=current_dir, check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def start_server(config: ConfigManager):
    """Start the web server"""
    # current_dir is already the web directory
    server_script = current_dir / "server.js"
    
    if not server_script.exists():
        print("❌ server.js not found in web directory")
        return False
    
    print("Starting Robot Platform Environment Web GUI on http://localhost:3000")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Start the server
        process = subprocess.Popen(
            ['node', 'server.js'],
            cwd=current_dir,
            env={
                **os.environ,
                'PORT': '3000',
                'HOST': 'localhost'
            }
        )
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        print("\nStopping server...")
        if process:
            process.terminate()
            process.wait()
        print("Server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True


def main():
    """Main entry point"""
    # Check prerequisites
    if not check_nodejs():
        print("❌ Node.js is not installed")
        print("Please install Node.js from https://nodejs.org/")
        sys.exit(1)
    
    if not check_npm():
        print("❌ npm is not installed")
        print("Please install npm (usually comes with Node.js)")
        sys.exit(1)
    
    # Load configuration
    config = ConfigManager()
    
    # Check if GUI is enabled
    if not config.get('GUI_ENABLED', True):
        print("❌ Web GUI is disabled in configuration")
        sys.exit(1)
    
    # Install dependencies if needed
    # current_dir is already the web directory
    node_modules = current_dir / "node_modules"
    
    if not node_modules.exists():
        if not install_dependencies():
            sys.exit(1)
    
    # Start the server
    if not start_server(config):
        sys.exit(1)


if __name__ == "__main__":
    main() 