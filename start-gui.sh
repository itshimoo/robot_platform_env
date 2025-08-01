#!/bin/bash
# RobotLab Web GUI Starter Script

echo "🚀 Starting RobotLab Web GUI..."
echo "📁 Current directory: $(pwd)"

# Check if we're in the robot_platform_env directory
if [ ! -f "platform.env" ]; then
    echo "❌ Error: platform.env not found. Please run this script from the robot_platform_env directory."
    exit 1
fi

# Check if web directory exists
if [ ! -d "web" ]; then
    echo "❌ Error: web directory not found."
    exit 1
fi

# Start the web GUI
echo "🌐 Starting web server..."
cd web
python3 rpe-webgui.py 