#!/usr/bin/env python3
"""
RobotLab Web GUI Launcher
"""

import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    """Start the RobotLab Web GUI"""
    print("🚀 Starting RobotLab Web GUI...")
    
    # Get the web directory (script is already in web directory)
    web_dir = Path(__file__).parent
    
    if not web_dir.exists():
        print("❌ Web directory not found")
        sys.exit(1)
    
    # Check if Node.js is installed
    try:
        subprocess.run(["node", "--version"], 
                      check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is not installed. Please install Node.js to "
              "run the web GUI.")
        sys.exit(1)
    
    # Check if npm dependencies are installed
    node_modules = web_dir / "node_modules"
    
    if not node_modules.exists():
        print("📦 Installing npm dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd=web_dir, check=True)
        except subprocess.CalledProcessError:
            print("❌ Failed to install npm dependencies")
            sys.exit(1)
    
    # Check if port 3000 is already in use
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 3000))
        sock.close()
        
        if result == 0:
            print("⚠️  Port 3000 is already in use")
            print("🔄 Attempting to kill existing process...")
            try:
                subprocess.run(["pkill", "-f", "node.*server.js"], 
                              capture_output=True)
                time.sleep(2)
            except Exception:
                pass
    except ImportError:
        pass  # socket module not available
    
    # Start the web server
    print("🌐 Starting web server on http://localhost:3000")
    try:
        # Start the server in the background
        process = subprocess.Popen(
            ["npm", "start"], 
            cwd=web_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if the server is running
        try:
            import requests
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ Web GUI is running!")
                print("🌐 Open your browser to: http://localhost:3000")
                
                # Try to open the browser
                try:
                    webbrowser.open("http://localhost:3000")
                    print("🔗 Browser opened automatically")
                except Exception:
                    print("💡 Please manually open: http://localhost:3000")
                
                print("\n🛑 Press Ctrl+C to stop the server")
                
                # Keep the script running
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping web server...")
                    process.terminate()
                    process.wait()
                    print("✅ Web server stopped")
                    
            else:
                print("❌ Web server failed to start properly")
                process.terminate()
                sys.exit(1)
                
        except ImportError:
            print("⚠️  requests module not available, skipping health check")
            print("🌐 Open your browser to: http://localhost:3000")
            process.wait()
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start web server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 