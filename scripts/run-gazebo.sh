#!/bin/bash
# Run Gazebo with X11 forwarding and ROS master

echo "🌍 Starting Gazebo with X11 forwarding and ROS master..."
echo "========================================================"

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

# Start ROS master in background if not running
echo "🚀 Starting ROS master..."
docker exec -d \
    robotlab-container \
    bash -c "source /opt/ros/noetic/setup.bash && roscore"

# Wait a moment for ROS master to start
sleep 2

# Run Gazebo in the container
echo "🚀 Launching Gazebo..."
docker exec \
    -e DISPLAY="$DISPLAY" \
    robotlab-container \
    bash -c "source /opt/ros/noetic/setup.bash && gazebo" 