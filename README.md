# Robot Platform Environment - Docker-based ROS Environment Manager

## Overview

Robot Platform Environment is a comprehensive system for managing Docker-based ROS (Robot Operating System) environments. It provides both command-line interface (CLI) tools and a graphical user interface (GUI) for building, running, and managing ROS containers. The system emphasizes dynamic configuration, cross-platform compatibility, and ease of use through automated setup and deployment scripts.

## Features

- **Docker-based ROS Environments**: Isolated ROS development environments using Docker containers
- **Dual Interface**: Both CLI and modern web-based GUI for system management
- **Real-time Monitoring**: Live container status and console output monitoring
- **Cross-platform Compatibility**: Works across different Linux distributions
- **Dynamic Configuration**: Environment-based configuration with automatic path detection
- **Auto-completion Support**: Bash completion for CLI commands
- **Modular Architecture**: Separated concerns with specialized managers

## Quick Start

### Prerequisites

- Linux operating system
- Docker installed and running
- Python 3.6+
- Node.js 14+ (for web GUI)
- Git

### Installation

#### Simple 3-Step Process

1. **Clone the repository:**
```bash
git clone <repository-url>
cd robot_platform_env
```

2. **Configure your robot (optional):**
```bash
# Copy example config and customize
cp platform.env.example platform.env
nano platform.env
```

3. **Install with one command:**
```bash
./install.sh platform.env
```

#### Configuration File (platform.env)
Your control center for robot platform configuration - just 15 lines:

```bash
# Robot Identity
ROBOT_NAME=my_robot
ROBOT_TYPE=mobile_robot
ROS_DISTRO=noetic

# Docker Settings
DOCKER_IMAGE=my_robot_ros
DOCKER_CONTAINER=my_robot_container
DOCKER_PORT=8080

# Hardware Configuration
HAS_CAMERA=true
HAS_LIDAR=true
MOTOR_COUNT=4

# CLI Configuration
CLI_COMMAND=rpe

# Development Settings
GUI_ENABLED=true
DEBUG_MODE=false
```

#### Alternative Installation Methods

**Option 1: Use default configuration**
```bash
./install.sh  # Uses default platform.env
```

**Option 2: Custom configuration file**
```bash
./install.sh my_platform.env  # Use your custom config
```

**Option 3: Step-by-step (advanced)**
```bash
./scripts/env-setup.sh  # Install prerequisites
./scripts/setup.sh      # Install Robot Platform Environment
```

#### Start the System
```bash
# CLI mode (using default command)
rpe build
rpe run

# CLI mode (using custom command from platform.env)
myrobot build    # if CLI_COMMAND=myrobot
rosbot run       # if CLI_COMMAND=rosbot
xi shell         # if CLI_COMMAND=xi

# GUI mode
rpe webgui  # or your custom command
```

## System Architecture

### Simple Configuration System
- **Robot-Focused**: Simple .env file for robot configuration
- **Easy Customization**: Just 15 lines to configure your robot
- **Standard Format**: Uses .env format (no dependencies)
- **Perfect for Robotics**: Works with Docker, ROS, and robotics tools
- **Environment Variables**: Can override with export commands

### CLI Customization
- **Custom Command Names**: Change the CLI command via `CLI_COMMAND` in robot.env
- **Personalized Experience**: Use your own command name (e.g., `myrobot`, `rosbot`, `autobot`)
- **Automatic Updates**: Help text and examples update automatically
- **Bash Completion**: Custom command gets proper tab completion

### Frontend Architecture
- **Web GUI Application**: Modern web-based interface with Node.js backend
  - Express.js server with Socket.IO for real-time communication
  - Responsive HTML/CSS/JavaScript frontend with modern design
  - Real-time container status monitoring and control
  - Live console output with color-coded messages
  - Cross-platform compatibility (runs in any web browser)
  - Support for custom command execution

### Backend Architecture
- **Modular Utility System**: Python-based backend with specialized managers
  - `ConfigManager`: Handles environment configuration and Docker file generation
  - `DockerManager`: Manages Docker container operations and status monitoring
  - `PathDetector`: Provides dynamic path detection for cross-platform compatibility
  - `ProjectConfig`: Centralized configuration management
- **CLI Integration**: Bash-based command-line tools with auto-completion support

## Key Components

### 1. Configuration Manager (`src/utils/config_manager.py`)
- Environment file parsing with support for comments and quotes
- Boolean value conversion
- Template-based Docker file generation
- Configuration validation and error handling

### 2. Docker Manager (`src/utils/docker_manager.py`)
- Container build, run, stop, and status operations
- Image management and cleanup
- Configuration-based container naming
- Command execution with proper error handling

### 3. Path Detector (`src/utils/path_detector.py`)
- Dynamic user and system binary directory detection
- Bash completion directory detection
- Sudo access checking and fallback mechanisms
- Path creation with proper permissions

### 4. Web GUI Application (`webgui-cli.py`, `web/server.js`)
- Node.js/Express server with Socket.IO for real-time updates
- Responsive web interface with modern gradient design
- Real-time container status monitoring and control buttons
- Live console output with color-coded command execution
- Configuration display and custom command interface

## Usage

### CLI Commands

```bash
# Build ROS container
rpe build

# Run container
rpe run

# Stop container
rpe stop

# Check status
rpe status

# View logs
rpe logs

# Shell into container
rpe shell

# Start web GUI
rpe webgui

# Show help
rpe --help
```

### Web GUI

1. Start the web GUI:
```bash
robotlab webgui
```

2. Open your browser and navigate to `http://localhost:3000`

3. Use the web interface to:
   - Monitor container status
   - Start/stop containers
   - View real-time console output
   - Execute custom commands
   - View system configuration

## Customization

### Renaming the Project
RobotLab uses a centralized configuration system that makes it easy to rename the entire project:

#### Option 1: Edit Configuration File
1. Edit `src/utils/project_config.py`
2. Change the values in the `ProjectConfig` class:
   ```python
   PROJECT_NAME = "myros"
   PROJECT_DISPLAY_NAME = "MyROS"
   CLI_COMMAND_NAME = "myros"
   DOCKER_IMAGE_NAME = "myros-ros"
   DOCKER_CONTAINER_NAME = "myros-container"
   ```
3. All scripts will automatically use the new names

#### Option 2: Environment Variables
Override settings without code changes:
```bash
export ROBOTLAB_PROJECT_NAME="myros"
export ROBOTLAB_DISPLAY_NAME="MyROS"
export ROBOTLAB_CLI_COMMAND_NAME="myros"
```

#### Demo Scripts
- `python3 demo_config.py` - Show current configuration
- `./scripts/rename_project.sh` - Interactive renaming demo

### Benefits
- ✅ **Single Source of Truth**: All names in one place
- ✅ **Easy Rebranding**: Change project name instantly
- ✅ **Consistent Naming**: All components use same configuration
- ✅ **No Hardcoded Strings**: Eliminates scattered project names
- ✅ **Environment Override**: Customize without code changes

## Configuration

The system uses a **centralized configuration system** located in `src/utils/project_config.py`. All project names and settings are defined in one place, making it easy to customize and maintain.

### Key Configuration Values:
- `PROJECT_NAME`: Base name for the project
- `PROJECT_DISPLAY_NAME`: Human-readable project name
- `CLI_COMMAND_NAME`: Command-line interface name
- `DOCKER_IMAGE_NAME`: Name of the Docker image
- `DOCKER_CONTAINER_NAME`: Name of the container
- `ROS_DISTRO`: ROS distribution (e.g., noetic, melodic)
- `WEB_PORT`: Port for the web GUI
- `DOCKER_PORT`: Port for Docker container

## Development

### Project Structure

```
robotlab/
├── .project.env              # Main configuration file
├── README.md                 # This file
├── src/
│   ├── utils/               # Utility modules
│   │   ├── config_manager.py
│   │   ├── docker_manager.py
│   │   └── path_detector.py
│   ├── cli/                 # CLI components
│   └── gui/                 # GUI components
├── templates/               # Docker templates
├── web/                    # Web GUI files
├── scripts/                # Setup and utility scripts
└── completion/             # Bash completion files
```

### Adding New Features

1. **CLI Commands**: Add new commands in `src/cli/`
2. **Web GUI**: Extend the web interface in `web/`
3. **Utilities**: Add utility functions in `src/utils/`
4. **Templates**: Add Docker templates in `templates/`

## Troubleshooting

### Common Issues

1. **Docker not running**: Ensure Docker daemon is started
2. **Permission errors**: Check if user is in docker group
3. **Port conflicts**: Change ports in `.project.env`
4. **Python import errors**: Ensure PYTHONPATH is set correctly

### Debug Mode

Enable debug mode in `.project.env`:
```
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Recent Updates

### CLI Python Import Issue Resolution
- **Date**: July 29, 2025
- **Issue**: CLI commands failing with "ModuleNotFoundError: No module named 'utils'"
- **Root Cause**: Incorrect Python path setup in CLI script preventing import of utility modules
- **Fix Applied**: Updated CLI script to use proper PYTHONPATH environment variable for Python module imports
- **Commands Fixed**: `build`, `status`, and other CLI commands that use Python utilities
- **Impact**: All CLI functionality now works correctly after setup installation 