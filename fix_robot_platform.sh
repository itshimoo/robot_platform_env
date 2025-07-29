#!/bin/bash
# Robot Platform Environment Fix Script
# Addresses the main issues identified in the installation

set -e  # Exit on any error

echo "🤖 Robot Platform Environment Fix Script"
echo "========================================"
echo ""

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

# Check if we're in the right directory
if [ ! -f "rpe" ] && [ ! -f "autobot" ]; then
    print_error "Not in robot platform environment directory"
    print_status "Please run this script from the robot_platform_env directory"
    exit 1
fi

print_status "Starting fixes..."

# Fix 1: Check and fix webgui script
print_status "Fix 1: Checking webgui script..."
if [ -f "rpe-webgui.py" ]; then
    chmod +x rpe-webgui.py
    print_success "WebGUI script found and made executable"
else
    print_error "rpe-webgui.py not found"
    exit 1
fi

# Fix 2: Check Node.js version
print_status "Fix 2: Checking Node.js version..."
NODE_VERSION=$(node --version 2>/dev/null | cut -d'v' -f2 | cut -d'.' -f1)
if [ -z "$NODE_VERSION" ]; then
    print_error "Node.js not installed"
    print_status "Please install Node.js v14+ manually"
elif [ "$NODE_VERSION" -lt 14 ]; then
    print_warning "Node.js version $NODE_VERSION is too old (need v14+)"
    print_status "Please upgrade Node.js to v14+ manually"
else
    print_success "Node.js version $NODE_VERSION is compatible"
fi

# Fix 3: Check web dependencies
print_status "Fix 3: Checking web dependencies..."
if [ -d "web" ] && [ -f "web/package.json" ]; then
    cd web
    if [ -d "node_modules" ]; then
        print_success "Web dependencies already installed"
    else
        print_status "Installing web dependencies..."
        npm install
        print_success "Web dependencies installed"
    fi
    cd ..
else
    print_error "Web directory or package.json not found"
fi

# Fix 4: Check CLI command consistency
print_status "Fix 4: Checking CLI command consistency..."
if command -v autobot >/dev/null 2>&1; then
    CLI_CMD="autobot"
    print_success "Using autobot command"
elif command -v rpe >/dev/null 2>&1; then
    CLI_CMD="rpe"
    print_success "Using rpe command"
elif [ -f "./rpe" ] && [ -x "./rpe" ]; then
    CLI_CMD="./rpe"
    print_success "Using local rpe script"
else
    print_error "No CLI command found"
    exit 1
fi

# Fix 5: Test CLI commands
print_status "Fix 5: Testing CLI commands..."
if $CLI_CMD --help >/dev/null 2>&1; then
    print_success "CLI help command works"
else
    print_error "CLI help command failed"
fi

if $CLI_CMD config >/dev/null 2>&1; then
    print_success "CLI config command works"
else
    print_error "CLI config command failed"
fi

# Fix 6: Check web server configuration
print_status "Fix 6: Checking web server configuration..."
if [ -f "web/server.js" ]; then
    # Check if server.js references the correct CLI command
    if grep -q "robotlab" web/server.js; then
        print_warning "Web server may reference wrong script name"
        print_status "You may need to update web/server.js to use '$CLI_CMD'"
    else
        print_success "Web server configuration looks correct"
    fi
else
    print_error "web/server.js not found"
fi

# Fix 7: Test Python modules
print_status "Fix 7: Testing Python modules..."
if python3 -c "import sys; sys.path.insert(0, 'src'); from utils.config_manager import ConfigManager; print('Python modules OK')" 2>/dev/null; then
    print_success "Python modules working correctly"
else
    print_error "Python modules import failed"
fi

# Fix 8: Check Docker
print_status "Fix 8: Checking Docker..."
if command -v docker >/dev/null 2>&1; then
    if docker ps >/dev/null 2>&1; then
        print_success "Docker is accessible"
    else
        print_warning "Docker installed but not accessible (may need sudo or group membership)"
    fi
else
    print_error "Docker not installed"
fi

# Fix 9: Test webgui command
print_status "Fix 9: Testing webgui command..."
if $CLI_CMD webgui --help >/dev/null 2>&1; then
    print_success "WebGUI command works"
else
    print_error "WebGUI command failed"
    print_status "This is the main issue you reported"
    print_status "The webgui script path may be incorrect in the CLI command"
fi

echo ""
echo "========================================"
print_status "Fix script completed!"
echo ""

# Summary
echo "📊 SUMMARY:"
echo "==========="
echo "✅ WebGUI script: $(if [ -x "rpe-webgui.py" ]; then echo "OK"; else echo "ISSUE"; fi)"
echo "✅ Node.js: $(if [ "$NODE_VERSION" -ge 14 ] 2>/dev/null; then echo "OK"; else echo "NEEDS UPGRADE"; fi)"
echo "✅ Web dependencies: $(if [ -d "web/node_modules" ]; then echo "OK"; else echo "MISSING"; fi)"
echo "✅ CLI command: $CLI_CMD"
echo "✅ Python modules: $(if python3 -c "import sys; sys.path.insert(0, 'src'); from utils.config_manager import ConfigManager" 2>/dev/null; then echo "OK"; else echo "ISSUE"; fi)"
echo "✅ Docker: $(if docker ps >/dev/null 2>&1; then echo "OK"; else echo "ISSUE"; fi)"
echo "✅ WebGUI command: $(if $CLI_CMD webgui --help >/dev/null 2>&1; then echo "OK"; else echo "ISSUE"; fi)"

echo ""
print_status "Next steps:"
echo "1. If Node.js needs upgrade: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs"
echo "2. If webgui command fails: Check the script path in your CLI command"
echo "3. Test the web GUI: $CLI_CMD webgui"
echo "4. Access web interface: http://localhost:3000"

echo ""
print_success "Fix script completed! 🚀"