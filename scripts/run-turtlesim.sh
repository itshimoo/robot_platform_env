#!/bin/bash
# Run turtlesim with X11 forwarding

echo "🐢 Starting turtlesim with X11 forwarding..."
echo "============================================="

# Check if container is running
if ! docker ps --format "table {{.Names}}" | grep -q "robotlab-container"; then
    echo "❌ RobotLab container is not running"
    echo "💡 Start it first with: rpe run"
    exit 1
fi

# Check if DISPLAY is set
if [ -z "$DISPLAY" ]; then
    echo "❌ DISPLAY environment variable is not set"
    echo "💡 Make sure you're running in a GUI environment"
    exit 1
fi

# Set up X11 permissions
echo "🔓 Setting up X11 permissions..."
xhost +local: 2>/dev/null

# Run turtlesim in the container
echo "🚀 Launching turtlesim..."
docker exec \
    -e DISPLAY="$DISPLAY" \
    robotlab-container \
    bash -c "source /opt/ros/noetic/setup.bash && rosrun turtlesim turtlesim_node" 