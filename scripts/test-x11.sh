#!/bin/bash
# Test X11 forwarding and GUI applications

echo "🔍 Testing X11 forwarding for GUI applications..."
echo "================================================"

# Check if DISPLAY is set
if [ -z "$DISPLAY" ]; then
    echo "❌ DISPLAY environment variable is not set"
    echo "💡 Make sure you're running in a GUI environment"
    exit 1
fi

echo "✅ DISPLAY is set to: $DISPLAY"

# Check if xhost is available
if ! command -v xhost >/dev/null 2>&1; then
    echo "❌ xhost command not found"
    echo "💡 Install x11-utils package: sudo apt install x11-utils"
    exit 1
fi

# Set up X11 permissions
echo "🔓 Setting up X11 permissions..."
xhost +local: 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ X11 permissions configured"
else
    echo "❌ Failed to set X11 permissions"
    exit 1
fi

# Check if container is running
if ! docker ps --format "table {{.Names}}" | grep -q "robotlab-container"; then
    echo "❌ RobotLab container is not running"
    echo "💡 Start it first with: rpe run"
    exit 1
fi

echo "✅ RobotLab container is running"

# Test X11 forwarding with a simple GUI application
echo "🧪 Testing X11 forwarding with xeyes..."
docker exec \
    -e DISPLAY="$DISPLAY" \
    robotlab-container \
    bash -c "apt update && apt install -y x11-apps && timeout 5 xeyes" &

sleep 3

# Check if xeyes started successfully
if pgrep -f "xeyes" >/dev/null; then
    echo "✅ X11 forwarding test successful!"
    echo "🎉 GUI applications should now work properly"
    echo ""
    echo "💡 You can now run GUI applications like:"
    echo "   • rpe rviz"
    echo "   • rosrun turtlesim turtlesim_node"
    echo "   • rosrun rviz rviz"
else
    echo "❌ X11 forwarding test failed"
    echo "💡 Check your X11 setup and try again"
fi

echo ""
echo "🔧 Troubleshooting tips:"
echo "   • Make sure you're running in a GUI environment (not SSH without X11 forwarding)"
echo "   • Try running: xhost +local:"
echo "   • Check if /tmp/.X11-unix exists and is accessible"
echo "   • Restart your container: rpe stop && rpe run" 