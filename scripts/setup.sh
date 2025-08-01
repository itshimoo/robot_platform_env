#!/bin/bash

# RobotLab Setup Script
# Installs RobotLab system-wide with proper path detection and permissions

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect installation paths
detect_paths() {
    print_status "Detecting installation paths..."
    
    # Detect install path
    if [ -w "/usr/local/bin" ]; then
        INSTALL_PATH="/usr/local/bin"
    elif [ -w "/usr/bin" ]; then
        INSTALL_PATH="/usr/bin"
    else
        INSTALL_PATH="$HOME/.local/bin"
        mkdir -p "$INSTALL_PATH"
    fi
    
    # Detect completion path
    if [ -w "/etc/bash_completion.d" ]; then
        COMPLETION_PATH="/etc/bash_completion.d"
    elif [ -w "/usr/share/bash-completion/completions" ]; then
        COMPLETION_PATH="/usr/share/bash-completion/completions"
    else
        COMPLETION_PATH="$HOME/.bash_completion.d"
        mkdir -p "$COMPLETION_PATH"
    fi
    
    # Detect config path
    if [ -w "/etc" ]; then
        CONFIG_PATH="/etc/robotlab"
    else
        CONFIG_PATH="$HOME/.config/robotlab"
    fi
    
    print_success "Install path: $INSTALL_PATH"
    print_success "Completion path: $COMPLETION_PATH"
    print_success "Config path: $CONFIG_PATH"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_deps=false
    
    # Check Python
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed"
        missing_deps=true
    fi
    
    # Check Docker
    if ! command_exists docker; then
        print_error "Docker is not installed"
        missing_deps=true
    else
        # Check if user is in docker group
        if ! groups $USER | grep -q docker; then
            print_warning "User is not in docker group. You may need to run docker commands with sudo."
            print_warning "To add user to docker group: sudo usermod -aG docker $USER"
        fi
    fi
    
    # Check Node.js (optional for web GUI)
    if ! command_exists node; then
        print_error "Node.js is not installed. Web GUI will not be available."
        missing_deps=true
    fi
    
    # Check npm
    if ! command_exists npm; then
        print_error "npm is not installed. Web GUI will not be available."
        missing_deps=true
    fi
    
    if [ "$missing_deps" = true ]; then
        print_error "Missing prerequisites detected!"
        echo ""
        print_status "You can run the environment setup script to install missing dependencies:"
        print_status "  ./scripts/env-setup.sh"
        echo ""
        read -p "Would you like to run the environment setup script now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ./scripts/env-setup.sh
            # Re-check after environment setup
            check_prerequisites
        else
            print_error "Please install missing prerequisites manually and run setup again."
            exit 1
        fi
    else
        print_success "All prerequisites are installed"
    fi
}

# Function to install RobotLab
install_robotlab() {
    print_status "Installing Robot Platform Environment..."
    
    # Get the directory where this script is located
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
    
    # Get CLI command name from platform.env or use default
    if [ -f "platform.env" ]; then
        # Source platform.env to get CLI_COMMAND
        export $(grep -v '^#' platform.env | xargs)
        CLI_COMMAND="${CLI_COMMAND:-robotlab}"
    else
        CLI_COMMAND="${CLI_COMMAND:-robotlab}"
    fi
    
    # Create config directory
    mkdir -p "$CONFIG_PATH"
    
    # Copy configuration file
    if [ -f "$PROJECT_DIR/.project.env" ]; then
        cp "$PROJECT_DIR/.project.env" "$CONFIG_PATH/"
        print_success "Configuration copied to $CONFIG_PATH"
    fi
    
    # Make rpe script executable
    chmod +x "$PROJECT_DIR/bin/rpe"
    chmod +x "$PROJECT_DIR/web/rpe-webgui.py"
    
    # Create or update the CLI symlink
    if [ -w "$INSTALL_PATH" ]; then
        # Remove any existing rpe symlink (we'll replace it with the custom one)
        if [ -L "$INSTALL_PATH/rpe" ]; then
            rm "$INSTALL_PATH/rpe"
        fi
        
        # Remove the new CLI command symlink if it exists
        if [ -L "$INSTALL_PATH/$CLI_COMMAND" ]; then
            rm "$INSTALL_PATH/$CLI_COMMAND"
        fi
        
        # Create the symlink with the custom command name
        ln -sf "$PROJECT_DIR/bin/rpe" "$INSTALL_PATH/$CLI_COMMAND"
        print_success "Created symlink: $INSTALL_PATH/$CLI_COMMAND"
        
        # If CLI_COMMAND is not 'rpe', also create an 'rpe' symlink for backward compatibility
        if [ "$CLI_COMMAND" != "rpe" ]; then
            ln -sf "$PROJECT_DIR/bin/rpe" "$INSTALL_PATH/rpe"
            print_success "Created backward compatibility symlink: $INSTALL_PATH/rpe"
        fi
        
        # Install hyphenated command scripts
        print_status "Installing hyphenated commands..."
        for cmd in build run stop status logs shell webgui config update clean gpu rviz workspace; do
            if [ -f "$PROJECT_DIR/bin/$cmd" ]; then
                ln -sf "$PROJECT_DIR/bin/$cmd" "$INSTALL_PATH/$CLI_COMMAND-$cmd"
                print_success "Created hyphenated command: $INSTALL_PATH/$CLI_COMMAND-$cmd"
            fi
        done
    else
        print_warning "Cannot write to $INSTALL_PATH. Using local installation."
        print_warning "Add $PROJECT_DIR to your PATH or run from project directory."
    fi
    
    # Install bash completion
    if [ -f "$PROJECT_DIR/completion/rpe" ]; then
        # Remove old completion files that might be from previous installations
        # (only remove files that look like our CLI completion files)
        for old_file in "$COMPLETION_PATH"/*; do
            if [ -f "$old_file" ] && [ "$(basename "$old_file")" != "$CLI_COMMAND" ] && [ "$(basename "$old_file")" != "robotlab" ]; then
                rm -f "$old_file"
            fi
        done
        
        # Install completion for the current CLI command
        cp "$PROJECT_DIR/completion/rpe" "$COMPLETION_PATH/$CLI_COMMAND"
        print_success "Bash completion installed for $CLI_COMMAND"
        
        # Also install for rpe for backward compatibility
        if [ "$CLI_COMMAND" != "rpe" ]; then
            cp "$PROJECT_DIR/completion/rpe" "$COMPLETION_PATH/rpe"
            print_success "Bash completion installed for rpe (backward compatibility)"
        fi
    fi
    
    # Ensure PATH is in profile
    if [[ ":$PATH:" != *":$INSTALL_PATH:"* ]]; then
        if [ -f "$HOME/.bashrc" ]; then
            echo "" >> "$HOME/.bashrc"
            echo "# RobotLab PATH" >> "$HOME/.bashrc"
            echo "export PATH=\"$INSTALL_PATH:\$PATH\"" >> "$HOME/.bashrc"
            print_success "Added PATH to ~/.bashrc"
        fi
        
        if [ -f "$HOME/.bash_profile" ]; then
            echo "" >> "$HOME/.bash_profile"
            echo "# RobotLab PATH" >> "$HOME/.bash_profile"
            echo "export PATH=\"$INSTALL_PATH:\$PATH\"" >> "$HOME/.bash_profile"
            print_success "Added PATH to ~/.bash_profile"
        fi
    fi
}

# Function to install web dependencies
install_web_dependencies() {
    if command_exists npm && [ -f "$PROJECT_DIR/web/package.json" ]; then
        print_status "Installing web dependencies..."
        cd "$PROJECT_DIR/web"
        npm install
        print_success "Web dependencies installed"
    fi
}

# Function to test installation
test_installation() {
    print_status "Testing installation..."
    
    # Get CLI command name from environment or use default
    CLI_COMMAND="${CLI_COMMAND:-robotlab}"
    
    # Test CLI command
    if command_exists "$CLI_COMMAND"; then
        print_success "$CLI_COMMAND command is available"
        "$CLI_COMMAND" --help > /dev/null 2>&1 && print_success "$CLI_COMMAND command works correctly"
    else
        print_warning "$CLI_COMMAND command not found in PATH"
        print_warning "Try running: $PROJECT_DIR/rpe --help"
    fi
    
    # Test Python modules
    cd "$PROJECT_DIR"
    if python3 -c "import sys; sys.path.insert(0, 'src'); from utils.config_manager import ConfigManager; print('Python modules OK')" 2>/dev/null; then
        print_success "Python modules are working"
    else
        print_error "Python modules test failed"
        exit 1
    fi
}

# Function to show post-installation instructions
show_instructions() {
    # Get CLI command name from environment or use default
    CLI_COMMAND="${CLI_COMMAND:-robotlab}"
    
    echo ""
    print_success "Robot Platform Environment installation completed!"
    echo ""
    echo "Next steps:"
    echo "1. Restart your terminal or run: source ~/.bashrc"
    echo "2. Test the installation: $CLI_COMMAND --help"
    echo "3. Build your first container: $CLI_COMMAND build"
    echo "4. Start the web GUI: $CLI_COMMAND webgui"
    echo ""
    echo "Documentation: See README.md for more information"
    echo ""
}

# Main installation process
main() {
    echo "🤖 Robot Platform Environment Setup Script"
    echo "========================================="
    echo ""
    
    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root. This is not recommended for security reasons."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Run installation steps
    check_prerequisites
    detect_paths
    install_robotlab
    install_web_dependencies
    test_installation
    show_instructions
}

# Run main function
main "$@" 