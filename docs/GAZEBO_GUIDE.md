# Gazebo Simulation Guide

This guide explains how to run Gazebo simulations in the RobotLab platform environment.

## Overview

Gazebo is a powerful 3D simulation environment for robotics. The RobotLab platform includes Gazebo with ROS integration, allowing you to simulate robots, environments, and test your robotics applications.

## Prerequisites

1. **GUI Environment**: You must be running in a GUI environment
2. **X11 Forwarding**: Properly configured X11 forwarding (see GUI_APPLICATIONS.md)
3. **Container Running**: RobotLab container must be running
4. **ROS Master**: ROS master should be running (automatically started by scripts)

## Quick Start

### Method 1: Using the CLI Command

```bash
# Start Gazebo with ROS master
rx-gazebo
```

### Method 2: Using the Script

```bash
# Run the Gazebo script
./scripts/run-gazebo.sh
```

### Method 3: Manual Setup

```bash
# 1. Start ROS master
rx-shell
# Inside container:
roscore &

# 2. Start Gazebo
docker exec -e DISPLAY="$DISPLAY" robotlab-container \
    bash -c "source /opt/ros/noetic/setup.bash && gazebo"
```

## Available Gazebo Features

### Built-in Worlds

Gazebo comes with several example worlds:

- **Empty World**: `gazebo` (default)
- **ROS World**: `gazebo --verbose worlds/ros.world`
- **Robot Test World**: `gazebo --verbose worlds/robot_test.world`

### ROS Integration

Gazebo automatically integrates with ROS when you:

1. **Start ROS Master**: `roscore`
2. **Launch Gazebo**: `gazebo`
3. **Use ROS Topics**: Check available topics with `rostopic list`

## Common Gazebo Commands

### Basic Gazebo Operations

```bash
# Start Gazebo with empty world
gazebo

# Start with specific world
gazebo worlds/ros.world

# Start with verbose output
gazebo --verbose

# Start with GUI disabled (headless)
gazebo --headless
```

### ROS + Gazebo Integration

```bash
# Start ROS master
roscore

# In another terminal, start Gazebo
gazebo

# Check ROS topics
rostopic list

# Check Gazebo services
rosservice list
```

## Working with Robot Models

### Loading Robot Models

```bash
# Load a robot model (example with TurtleBot)
roslaunch turtlebot3_gazebo turtlebot3_world.launch

# Or manually spawn a robot
rosservice call /gazebo/spawn_urdf_model "model_name: 'my_robot'
model_xml: '<?xml version="1.0"?><robot name="simple_box"><link name="base_link"><visual><geometry><box size="1 1 1"/></geometry></visual></link></robot>'
initial_pose:
  position: {x: 0.0, y: 0.0, z: 0.5}
  orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}"
```

### Creating Custom Worlds

1. **Create a world file** (e.g., `my_world.world`):
```xml
<?xml version="1.0" ?>
<sdf version="1.4">
  <world name="default">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
    <!-- Add your custom models here -->
  </world>
</sdf>
```

2. **Launch with custom world**:
```bash
gazebo my_world.world
```

## Troubleshooting

### Common Issues

1. **"Could not connect to display"**
   - Check X11 forwarding: `./scripts/test-x11.sh`
   - Set permissions: `xhost +local:`

2. **"ROS master not running"**
   - Start ROS master: `roscore`
   - Or use the script: `./scripts/run-gazebo.sh`

3. **"Gazebo not found"**
   - Rebuild container: `rx-build`
   - Restart container: `rx-stop && rx-run`

4. **"Slow performance"**
   - Check GPU support: `rx-config`
   - Enable GPU: `rx-gpu`
   - Restart container

### Debugging Steps

1. **Check container status**:
   ```bash
   rx-status
   ```

2. **Check X11 forwarding**:
   ```bash
   ./scripts/test-x11.sh
   ```

3. **Check ROS master**:
   ```bash
   rx-shell
   # Inside container:
   rostopic list
   ```

4. **Check Gazebo installation**:
   ```bash
   rx-shell
   # Inside container:
   which gazebo
   gazebo --version
   ```

## Advanced Usage

### Running Multiple Simulations

```bash
# Terminal 1: Start ROS master
rx-shell
roscore

# Terminal 2: Start Gazebo
rx-gazebo

# Terminal 3: Run your robot nodes
rx-shell
rosrun your_package your_node
```

### Custom Gazebo Configuration

Create a custom Gazebo configuration:

```bash
# Create Gazebo config directory
mkdir -p ~/.gazebo

# Copy default models
cp -r /usr/share/gazebo-11/models ~/.gazebo/

# Create custom world
cat > ~/.gazebo/my_world.world << 'EOF'
<?xml version="1.0" ?>
<sdf version="1.4">
  <world name="default">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
  </world>
</sdf>
EOF
```

### Performance Optimization

1. **GPU Acceleration**: Enable GPU support in RobotLab
2. **Headless Mode**: Use `gazebo --headless` for server environments
3. **Model Caching**: Gazebo caches models in `~/.gazebo/models`
4. **Memory Management**: Close unused GUI applications

## Examples

### TurtleBot3 Simulation

```bash
# Install TurtleBot3 packages
rx-shell
sudo apt install ros-noetic-turtlebot3-gazebo

# Launch TurtleBot3 simulation
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

### Custom Robot Simulation

```bash
# 1. Create your robot package
rx-shell
cd /workspace/src
catkin_create_pkg my_robot_description urdf xacro

# 2. Add URDF files
# 3. Launch simulation
roslaunch my_robot_description gazebo.launch
```

### Sensor Simulation

```bash
# Add sensors to your robot model
# Example: Laser scanner, camera, IMU
# Then launch with sensor plugins
roslaunch my_robot_description gazebo_with_sensors.launch
```

## Integration with Other Tools

### RViz + Gazebo

```bash
# Terminal 1: Start ROS master and Gazebo
./scripts/run-gazebo.sh

# Terminal 2: Start RViz
rx-rviz
```

### rqt + Gazebo

```bash
# Terminal 1: Start Gazebo
rx-gazebo

# Terminal 2: Start rqt
docker exec -e DISPLAY="$DISPLAY" robotlab-container \
    bash -c "source /opt/ros/noetic/setup.bash && rosrun rqt_gui rqt_gui"
```

## Support

If you encounter issues:

1. **Check logs**: `rx-logs`
2. **Test X11**: `./scripts/test-x11.sh`
3. **Rebuild**: `rx-build`
4. **Restart**: `rx-stop && rx-run`
5. **Check documentation**: `docs/GUI_APPLICATIONS.md`

## Resources

- [Gazebo Documentation](http://gazebosim.org/docs)
- [ROS Gazebo Tutorials](http://wiki.ros.org/gazebo_ros)
- [RobotLab Platform Documentation](docs/) 