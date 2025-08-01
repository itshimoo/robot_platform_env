#!/bin/bash

# RobotLab One-Click Installation Script
# This script sets up your robot environment from a simple config file

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Function to check if config file exists
check_config_file() {
    local config_file="$1"
    
    if [ ! -f "$config_file" ]; then
        print_warning "Configuration file '$config_file' not found!"
        echo ""
        echo "Creating default configuration file..."
        cp platform.env.example "$config_file" 2>/dev/null || {
            print_warning "No example config found. Creating basic config..."
            cat > "$config_file" << 'EOF'
# RobotLab Configuration - Your Control Center
ROBOT_NAME=my_robot
ROBOT_TYPE=mobile_robot
ROS_DISTRO=noetic
DOCKER_IMAGE=my_robot_ros
DOCKER_CONTAINER=my_robot_container
DOCKER_PORT=8080
GUI_ENABLED=true
EOF
        }
        print_success "Created configuration file: $config_file"
        echo ""
        print_info "Edit '$config_file' to customize your robot setup"
        echo ""
    fi
}

# Function to load configuration
load_config() {
    local config_file="$1"
    
    if [ -f "$config_file" ]; then
        print_step "Loading configuration from $config_file"
        
        # Read and export variables from config file, ignoring comments and empty lines
        while IFS= read -r line; do
            # Skip empty lines and comments
            if [[ -n "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
                # Export the variable
                export "$line"
            fi
        done < "$config_file"
        
        print_success "Configuration loaded:"
        echo "  Robot: ${ROBOT_NAME:-'Not set'} (${ROBOT_TYPE:-'Not set'})"
        echo "  ROS: ${ROS_DISTRO:-'Not set'}"
        echo "  Docker: ${DOCKER_IMAGE:-'Not set'}:${DOCKER_CONTAINER:-'Not set'}"
        echo "  Port: ${DOCKER_PORT:-'Not set'}"
        echo ""
    fi
}

# Main installation function
main() {
    echo -e "${BLUE}🤖 Robot Platform Environment Installation${NC}"
    echo "================================================"
    echo ""
    
    # Get config file from command line or use default
    CONFIG_FILE="${1:-platform.env}"
    
    print_step "Using configuration file: $CONFIG_FILE"
    echo ""
    
    # Check if we're in the right directory
    if [ ! -f "scripts/setup.sh" ] || [ ! -f "scripts/env-setup.sh" ] || [ ! -f "bin/rpe" ]; then
        print_warning "Error: Please run this script from the Robot Platform Environment project directory"
        echo "Make sure you're in the directory containing the 'scripts' and 'bin' folders"
        exit 1
    fi
    
    # Check and create config file if needed
    check_config_file "$CONFIG_FILE"
    
    # Load configuration
    load_config "$CONFIG_FILE"
    
    print_step "Step 1: Setting up environment and installing prerequisites..."
    ./scripts/env-setup.sh
    
    echo ""
    print_step "Step 2: Installing Robot Platform Environment with your configuration..."
    ./scripts/setup.sh
    
    echo ""
    print_step "Step 3: Setting up Git-enhanced Bash prompt..."
    # Run the git bash prompt setup script
    if [ -f "git_bash_prompt_setup.sh" ]; then
        chmod +x git_bash_prompt_setup.sh
        ./git_bash_prompt_setup.sh
    else
        print_warning "git_bash_prompt_setup.sh not found. Skipping Git prompt setup."
    fi
    
    echo ""
    print_success "🎉 Robot Platform Environment installation completed successfully!"
    echo ""
    echo "Your robot configuration:"
    echo "  Robot: $ROBOT_NAME"
    echo "  Type: $ROBOT_TYPE"
    echo "  ROS: $ROS_DISTRO"
    echo "  Docker: $DOCKER_IMAGE"
    echo "  CLI Command: ${CLI_COMMAND:-robotlab}"
    echo ""
    echo "Next steps:"
    echo "1. Restart your terminal or run: source ~/.bashrc (to activate Git prompt)"
    echo "2. Test the installation: ${CLI_COMMAND:-robotlab} --help"
    echo "3. Build your robot container: ${CLI_COMMAND:-robotlab} build"
    echo "4. Start the web GUI: ${CLI_COMMAND:-robotlab} webgui"
    echo ""
    print_info "Configuration file: $CONFIG_FILE"
            print_info "Edit this file to customize your robot platform setup"
    echo ""
    echo "Happy robotics! 🚀"
}

# Run main function with command line arguments
main "$@" 