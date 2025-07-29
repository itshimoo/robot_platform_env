#!/bin/bash

# RobotLab Container Entrypoint
# This script is executed when the container starts

set -e

# Source ROS environment
source /opt/ros/$ROS_DISTRO/setup.bash

# Source workspace if it exists
if [ -f "/workspace/devel/setup.bash" ]; then
    source /workspace/devel/setup.bash
fi

# Set up environment variables
export ROS_HOSTNAME=$(hostname -I | awk '{print $1}')
export ROS_MASTER_URI=http://$ROS_HOSTNAME:11311

# Print welcome message
echo "🤖 Welcome to RobotLab ROS Environment"
echo "======================================"
echo "ROS Distribution: $ROS_DISTRO"
echo "ROS Version: $ROS_VERSION"
echo "Python Version: $PYTHON_VERSION"
echo "Workspace: /workspace"
echo "ROS Master: $ROS_MASTER_URI"
echo ""

# Check if workspace is initialized
if [ ! -d "/workspace/src" ]; then
    echo "📁 Initializing ROS workspace..."
    cd /workspace
    catkin init
    echo "✅ Workspace initialized"
fi

# Check if workspace needs to be built
if [ ! -d "/workspace/devel" ]; then
    echo "🔨 Building workspace..."
    cd /workspace
    catkin build
    echo "✅ Workspace built"
fi

# Show available ROS packages
echo "📦 Available ROS packages:"
rospack list | head -5
echo "..."

# Show workspace status
echo "📁 Workspace status:"
cd /workspace
catkin status --verbose 2>/dev/null || echo "No packages in workspace yet"

echo ""
echo "🚀 Ready for ROS development!"
echo "Try: roscore, rosrun turtlesim turtlesim_node, rviz"
echo ""

# Execute the command passed to the container
exec "$@" 