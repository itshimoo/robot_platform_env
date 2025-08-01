#!/bin/bash
# Test X11 forwarding in RobotLab container

echo "🧪 Testing X11 forwarding in RobotLab container..."

# Check if container is running
if ! docker ps | grep -q robotlab-container; then
    echo "❌ Container is not running. Please start it first with 'robocmd run'"
    exit 1
fi

# Check if DISPLAY is set
if [ -z "$DISPLAY" ]; then
    echo "❌ DISPLAY environment variable not set. Please run this in a GUI environment."
    exit 1
fi

echo "✅ Container is running"
echo "✅ DISPLAY is set to: $DISPLAY"

# Allow X11 connections
echo "🔓 Allowing X11 connections..."
xhost +local:

# Test with a simple X11 application
echo "🧪 Testing with xclock..."
docker exec -it -e DISPLAY=$DISPLAY robotlab-container bash -c "apt-get update && apt-get install -y x11-apps && xclock" &

echo "⏰ If you see a clock window, X11 forwarding is working!"
echo "🎯 You can now run RViz with: robocmd-rviz" 