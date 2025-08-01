# Robot Platform Environment - Repository Structure

## Overview
This repository is organized into logical directories for easy navigation and maintenance.

## Directory Structure

```
robot_platform_env/
├── README.md                    # Main project documentation
├── PROJECT_SUMMARY.md           # Project overview and features
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── Dockerfile                  # Main Docker image definition
├── platform.env                # Environment configuration
├── platform.env.example        # Example configuration
├── install.sh                  # Main installation script
│
├── bin/                        # CLI Commands
│   ├── rpe                     # Main CLI script
│   ├── build                   # Build command
│   ├── run                     # Run command
│   ├── stop                    # Stop command
│   ├── status                  # Status command
│   ├── logs                    # Logs command
│   ├── shell                   # Shell command
│   ├── webgui                  # Web GUI command
│   ├── config                  # Config command
│   ├── update                  # Update command
│   └── clean                   # Clean command
│
├── scripts/                    # Setup and Utility Scripts
│   ├── setup.sh               # Main setup script
│   ├── env-setup.sh           # Environment setup
│   ├── enable-buildkit.sh     # BuildKit enabler
│   ├── git_bash_prompt_setup.sh # Git prompt setup
│   └── entrypoint.sh          # Docker container entrypoint
│
├── src/                        # Python Source Code
│   └── utils/
│       ├── config_manager.py   # Configuration management
│       ├── docker_manager.py   # Docker operations
│       └── path_detector.py    # Path detection utilities
│
├── web/                        # Web GUI
│   ├── package.json           # Node.js dependencies
│   ├── server.js              # Web server
│   ├── rpe-webgui.py         # Web GUI Python script
│   └── public/                # Static web files
│
├── templates/                  # Docker Templates
│   └── Dockerfile.template    # Dockerfile template
│
├── completion/                 # Bash Completion
│   └── rpe                    # Bash completion script
│
├── tests/                      # Test Files
│   ├── test_cli.py           # CLI tests
│   ├── test_config_manager.py # Config manager tests
│   ├── test_docker_manager.py # Docker manager tests
│   └── test_path_detector.py # Path detector tests
│
└── docs/                       # Documentation
    └── STRUCTURE.md           # This file
```

## Key Benefits

### **Clean Organization**
- **bin/**: All CLI commands in one place
- **scripts/**: Setup and utility scripts organized
- **src/**: Python source code with clear structure
- **web/**: Web GUI components together
- **docs/**: Documentation centralized

### **Easy Navigation**
- **Root directory**: Only essential files
- **Logical grouping**: Related files together
- **Clear separation**: Different types of files in different directories

### **Maintainability**
- **Modular structure**: Easy to find and modify specific components
- **Scalable**: Easy to add new features in appropriate directories
- **Professional**: Follows standard project organization practices

## Usage

### **Installation**
```bash
./install.sh platform.env
```

### **CLI Commands**
```bash
# Hyphenated style (recommended)
robocmd-build
robocmd-run
robocmd-stop

# Traditional style (still works)
robocmd build
robocmd run
robocmd stop

# Note: The actual command name depends on your CLI_COMMAND setting
# If CLI_COMMAND=myrobot, you'd use: myrobot-build, myrobot-run, etc.
```

### **Development**
- **Python code**: Edit files in `src/`
- **CLI commands**: Modify files in `bin/`
- **Web GUI**: Work in `web/`
- **Scripts**: Update files in `scripts/` 