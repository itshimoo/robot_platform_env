# GUI Applications and X11 Forwarding

This document explains how to run GUI applications (like RViz, turtlesim, etc.) in the RobotLab container with proper X11 forwarding.

## Overview

The RobotLab platform supports running GUI applications inside Docker containers through X11 forwarding. This allows you to run ROS GUI tools like RViz, turtlesim, and other Qt-based applications.

## Prerequisites

1. **GUI Environment**: You must be running in a GUI environment (not SSH without X11 forwarding)
2. **X11 Utilities**: The `xhost` command must be available on your host system
3. **Container Running**: The RobotLab container must be running

## Quick Start

### 1. Test X11 Forwarding

First, test if X11 forwarding is working properly:

```bash
./scripts/test-x11.sh
```

This script will:
- Check if DISPLAY is set
- Set up X11 permissions
- Test with a simple GUI application (xeyes)
- Provide troubleshooting tips

### 2. Run RViz

Use the built-in RViz command:

```bash
rpe rviz
```

### 3. Run turtlesim

Use the provided script:

```bash
./scripts/run-turtlesim.sh
```

Or run it manually from the container shell:

```bash
rpe shell
# Inside the container:
rosrun turtlesim turtlesim_node
```

## Manual Setup

If you prefer to run GUI applications manually:

### 1. Set X11 Permissions

```bash
xhost +local:
```

### 2. Run GUI Application

```bash
docker exec -it \
    -e DISPLAY="$DISPLAY" \
    robotlab-container \
    bash -c "source /opt/ros/noetic/setup.bash && <your-gui-command>"
```

## Available GUI Applications

### ROS Applications

- **RViz**: `rpe rviz` or `rosrun rviz rviz`
- **turtlesim**: `./scripts/run-turtlesim.sh` or `rosrun turtlesim turtlesim_node`
- **rqt**: `rosrun rqt_gui rqt_gui`
- **PlotJuggler**: `rosrun plotjuggler plotjuggler`

### Testing Applications

- **xeyes**: `docker exec -it -e DISPLAY="$DISPLAY" robotlab-container xeyes`
- **xclock**: `docker exec -it -e DISPLAY="$DISPLAY" robotlab-container xclock`

## Troubleshooting

### Common Issues

1. **"could not connect to display"**
   - Make sure you're in a GUI environment
   - Check if DISPLAY is set: `echo $DISPLAY`
   - Run: `xhost +local:`

2. **"Qt platform plugin could not be initialized"**
   - Restart the container: `rpe stop && rpe run`
   - Check X11 permissions: `xhost +local:`

3. **"No protocol specified"**
   - Set X11 permissions: `xhost +local:`
   - Restart the container

### Debugging Steps

1. **Check DISPLAY variable**:
   ```bash
   echo $DISPLAY
   ```

2. **Check X11 permissions**:
   ```bash
   xhost
   ```

3. **Test with simple application**:
   ```bash
   ./scripts/test-x11.sh
   ```

4. **Check container status**:
   ```bash
   rpe status
   ```

5. **Restart container**:
   ```bash
   rpe stop
   rpe run
   ```

## Advanced Configuration

### Custom X11 Settings

If you need custom X11 settings, you can modify the Docker run command in `src/utils/docker_manager.py`:

```python
# Additional X11 security settings
'--security-opt', 'label=type:container_runtime_t',
```

### Multiple Displays

For systems with multiple displays, you can specify a different display:

```bash
export DISPLAY=:1
rpe rviz
```

### Remote X11 Forwarding

For remote connections, ensure X11 forwarding is enabled:

```bash
ssh -X user@remote-host
# or
ssh -Y user@remote-host
```

## Security Notes

- The `xhost +local:` command allows local connections to the X server
- This is generally safe for development environments
- For production systems, consider more restrictive X11 security settings

## Performance Tips

1. **Use X11 forwarding over SSH**: For remote connections, use `ssh -X` or `ssh -Y`
2. **Close unused GUI applications**: Each GUI application consumes resources
3. **Monitor system resources**: Use `htop` or `top` to monitor container performance

## Examples

### Running Multiple GUI Applications

```bash
# Terminal 1: Start turtlesim
./scripts/run-turtlesim.sh

# Terminal 2: Start RViz
rpe rviz

# Terminal 3: Start rqt
docker exec -it -e DISPLAY="$DISPLAY" robotlab-container \
    bash -c "source /opt/ros/noetic/setup.bash && rosrun rqt_gui rqt_gui"
```

### Custom GUI Application

```bash
# Run any Qt-based application
docker exec -it -e DISPLAY="$DISPLAY" robotlab-container \
    bash -c "source /opt/ros/noetic/setup.bash && your-gui-app"
```

## Support

If you encounter issues with GUI applications:

1. Run the test script: `./scripts/test-x11.sh`
2. Check the troubleshooting section above
3. Review the container logs: `rpe logs`
4. Restart the container: `rpe stop && rpe run` 