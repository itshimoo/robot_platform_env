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
src_dir = current_dir / "src"
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
    web_dir = current_dir / "web"
    package_json = web_dir / "package.json"
    
    if not package_json.exists():
        print("❌ package.json not found in web directory")
        return False
    
    print("Installing Node.js dependencies...")
    try:
        subprocess.run(['npm', 'install'], cwd=web_dir, check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def start_server(config: ConfigManager):
    """Start the web server"""
    web_dir = current_dir / "web"
    server_script = web_dir / "server.js"
    
    if not server_script.exists():
        print("❌ server.js not found in web directory")
        return False
    
    # Get configuration
    port = config.get('WEB_PORT', 3000)
    host = config.get('WEB_HOST', 'localhost')
    
    print(f"Starting Robot Platform Environment Web GUI on http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Start the server
        process = subprocess.Popen(
            ['node', 'server.js'],
            cwd=web_dir,
            env={
                **os.environ,
                'PORT': str(port),
                'HOST': host
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
    web_dir = current_dir / "web"
    node_modules = web_dir / "node_modules"
    
    if not node_modules.exists():
        if not install_dependencies():
            sys.exit(1)
    
    # Start the server
    if not start_server(config):
        sys.exit(1)


if __name__ == "__main__":
    main() 