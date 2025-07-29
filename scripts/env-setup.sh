#!/bin/bash

# Robot Platform Environment Setup Script
# Automatically installs all prerequisites for RobotLab

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    elif type lsb_release >/dev/null 2>&1; then
        OS=$(lsb_release -si)
        VER=$(lsb_release -sr)
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        OS=$DISTRIB_ID
        VER=$DISTRIB_RELEASE
    elif [ -f /etc/debian_version ]; then
        OS=Debian
        VER=$(cat /etc/debian_version)
    elif [ -f /etc/SuSe-release ]; then
        OS=SuSE
    elif [ -f /etc/redhat-release ]; then
        OS=RedHat
    else
        OS=$(uname -s)
        VER=$(uname -r)
    fi
    echo "$OS"
}

# Function to install Docker
install_docker() {
    print_step "Installing Docker..."
    
    if command_exists docker; then
        print_success "Docker is already installed"
        return 0
    fi
    
    OS=$(detect_os)
    
    case "$OS" in
        *"Ubuntu"*|*"Debian"*)
            print_status "Installing Docker on Ubuntu/Debian..."
            sudo apt-get update
            sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
            echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
            sudo apt-get update
            sudo apt-get install -y docker-ce docker-ce-cli containerd.io
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*)
            print_status "Installing Docker on CentOS/RHEL/Fedora..."
            sudo yum install -y yum-utils
            sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            sudo yum install -y docker-ce docker-ce-cli containerd.io
            ;;
        *"Arch"*)
            print_status "Installing Docker on Arch Linux..."
            sudo pacman -S --noconfirm docker
            ;;
        *)
            print_warning "Unsupported OS: $OS"
            print_warning "Please install Docker manually: https://docs.docker.com/get-docker/"
            return 1
            ;;
    esac
    
    # Start and enable Docker service
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    print_success "Docker installed successfully"
    print_warning "You may need to log out and back in for docker group changes to take effect"
}

# Function to install Node.js
install_nodejs() {
    print_step "Installing Node.js..."
    
    if command_exists node && command_exists npm; then
        NODE_VERSION=$(node --version)
        print_success "Node.js is already installed: $NODE_VERSION"
        return 0
    fi
    
    OS=$(detect_os)
    
    case "$OS" in
        *"Ubuntu"*|*"Debian"*)
            print_status "Installing Node.js on Ubuntu/Debian..."
            curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
            sudo apt-get install -y nodejs
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*)
            print_status "Installing Node.js on CentOS/RHEL/Fedora..."
            curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
            sudo yum install -y nodejs
            ;;
        *"Arch"*)
            print_status "Installing Node.js on Arch Linux..."
            sudo pacman -S --noconfirm nodejs npm
            ;;
        *)
            print_warning "Unsupported OS: $OS"
            print_warning "Please install Node.js manually: https://nodejs.org/"
            return 1
            ;;
    esac
    
    print_success "Node.js installed successfully"
}

# Function to install Python dependencies
install_python_deps() {
    print_step "Installing Python dependencies..."
    
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed"
        print_warning "Please install Python 3 manually"
        return 1
    fi
    
    # Install pip if not available
    if ! command_exists pip3; then
        print_status "Installing pip3..."
        OS=$(detect_os)
        case "$OS" in
            *"Ubuntu"*|*"Debian"*)
                sudo apt-get install -y python3-pip
                ;;
            *"CentOS"*|*"Red Hat"*|*"Fedora"*)
                sudo yum install -y python3-pip
                ;;
            *"Arch"*)
                sudo pacman -S --noconfirm python-pip
                ;;
        esac
    fi
    
    # Install Python packages if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        print_status "Installing Python packages from requirements.txt..."
        pip3 install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_status "No requirements.txt found, skipping Python package installation"
    fi
}

# Function to install system dependencies
install_system_deps() {
    print_step "Installing system dependencies..."
    
    OS=$(detect_os)
    
    case "$OS" in
        *"Ubuntu"*|*"Debian"*)
            print_status "Installing system packages on Ubuntu/Debian..."
            sudo apt-get update
            sudo apt-get install -y curl wget git build-essential
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*)
            print_status "Installing system packages on CentOS/RHEL/Fedora..."
            sudo yum install -y curl wget git gcc gcc-c++ make
            ;;
        *"Arch"*)
            print_status "Installing system packages on Arch Linux..."
            sudo pacman -S --noconfirm curl wget git base-devel
            ;;
    esac
    
    print_success "System dependencies installed"
}

# Function to verify installations
verify_installations() {
    print_step "Verifying installations..."
    
    local all_good=true
    
    # Check Docker
    if command_exists docker; then
        print_success "✓ Docker: $(docker --version)"
    else
        print_error "✗ Docker not found"
        all_good=false
    fi
    
    # Check Node.js
    if command_exists node; then
        print_success "✓ Node.js: $(node --version)"
    else
        print_error "✗ Node.js not found"
        all_good=false
    fi
    
    # Check npm
    if command_exists npm; then
        print_success "✓ npm: $(npm --version)"
    else
        print_error "✗ npm not found"
        all_good=false
    fi
    
    # Check Python
    if command_exists python3; then
        print_success "✓ Python: $(python3 --version)"
    else
        print_error "✗ Python 3 not found"
        all_good=false
    fi
    
    # Check Git
    if command_exists git; then
        print_success "✓ Git: $(git --version)"
    else
        print_error "✗ Git not found"
        all_good=false
    fi
    
    if [ "$all_good" = true ]; then
        print_success "All prerequisites verified successfully!"
        return 0
    else
        print_error "Some prerequisites are missing. Please install them manually."
        return 1
    fi
}

# Function to show post-installation instructions
show_instructions() {
    echo ""
    print_success "Environment setup completed!"
    echo ""
    echo "Next steps:"
    echo "1. If Docker was installed, log out and back in (or run: newgrp docker)"
    echo "2. Run the main setup script: ./scripts/setup.sh"
    echo "3. Test the installation: rpe --help"
    echo ""
    echo "Troubleshooting:"
    echo "- If Docker permission issues: sudo usermod -aG docker $USER"
    echo "- If Node.js issues: Check https://nodejs.org/"
    echo "- If Python issues: Check your Python 3 installation"
    echo ""
}

# Function to check if running as root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root. This is not recommended for security reasons."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Main function
main() {
    echo "🌍 Robot Platform Environment Setup"
    echo "==================================="
    echo ""
    
    check_root
    
    print_status "Detected OS: $(detect_os)"
    echo ""
    
    # Install all prerequisites
    install_system_deps
    install_docker
    install_nodejs
    install_python_deps
    
    echo ""
    verify_installations
    
    show_instructions
}

# Run main function
main "$@" 