#!/bin/bash

# RobotLab CI/CD Setup Script
# This script helps configure and manage the CI/CD pipeline

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

# Function to check if we're in a git repository
check_git_repo() {
    if [ ! -d ".git" ]; then
        print_error "Not in a git repository. Please run this script from the project root."
        exit 1
    fi
}

# Function to check GitHub CLI availability
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        print_warning "GitHub CLI not found. Install it for enhanced functionality:"
        echo "  https://cli.github.com/"
        return 1
    fi
    return 0
}

# Function to validate CI/CD setup
validate_setup() {
    print_status "Validating CI/CD setup..."
    
    # Check for workflow files
    if [ ! -d ".github/workflows" ]; then
        print_error "GitHub workflows directory not found"
        return 1
    fi
    
    # Check for required workflow files
    required_workflows=("ci.yml" "cd.yml" "security.yml" "quality.yml" "automation.yml")
    for workflow in "${required_workflows[@]}"; do
        if [ ! -f ".github/workflows/$workflow" ]; then
            print_error "Missing workflow file: $workflow"
            return 1
        fi
    done
    
    # Check for documentation
    if [ ! -f "docs/CI_CD.md" ]; then
        print_warning "CI/CD documentation not found"
    fi
    
    print_success "CI/CD setup validation complete"
    return 0
}

# Function to show CI/CD status
show_status() {
    print_status "CI/CD Pipeline Status"
    echo "========================"
    
    if check_gh_cli; then
        echo "Recent workflow runs:"
        gh run list --limit 5
    else
        echo "Install GitHub CLI to see workflow status:"
        echo "  https://cli.github.com/"
    fi
    
    echo ""
    echo "Available workflows:"
    echo "  - ci.yml: Main CI/CD pipeline"
    echo "  - cd.yml: Continuous deployment"
    echo "  - security.yml: Security scanning"
    echo "  - quality.yml: Quality assurance"
    echo "  - automation.yml: Automation & maintenance"
}

# Function to trigger manual workflow
trigger_workflow() {
    local workflow=$1
    local task=${2:-""}
    
    if ! check_gh_cli; then
        print_error "GitHub CLI required for manual workflow triggers"
        exit 1
    fi
    
    print_status "Triggering workflow: $workflow"
    
    if [ "$workflow" = "automation.yml" ] && [ -n "$task" ]; then
        gh workflow run "$workflow" -f task="$task"
        print_success "Triggered automation workflow with task: $task"
    else
        gh workflow run "$workflow"
        print_success "Triggered workflow: $workflow"
    fi
}

# Function to show workflow help
show_help() {
    echo "RobotLab CI/CD Setup Script"
    echo "=========================="
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  validate    - Validate CI/CD setup"
    echo "  status      - Show CI/CD status"
    echo "  trigger     - Trigger manual workflow"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 validate"
    echo "  $0 status"
    echo "  $0 trigger automation.yml update-deps"
    echo ""
    echo "Available automation tasks:"
    echo "  - all: Run all automation tasks"
    echo "  - update-deps: Update dependencies"
    echo "  - cleanup: Clean up resources"
    echo "  - security-update: Apply security updates"
}

# Function to check local environment
check_local_env() {
    print_status "Checking local development environment..."
    
    # Check Docker
    if command -v docker &> /dev/null; then
        print_success "Docker is available"
    else
        print_error "Docker not found. Install Docker for local development."
    fi
    
    # Check Python
    if command -v python3 &> /dev/null; then
        print_success "Python 3 is available"
    else
        print_error "Python 3 not found"
    fi
    
    # Check required files
    if [ -f "requirements.txt" ]; then
        print_success "requirements.txt found"
    else
        print_warning "requirements.txt not found"
    fi
    
    if [ -f "Dockerfile" ]; then
        print_success "Dockerfile found"
    else
        print_error "Dockerfile not found"
    fi
}

# Main script logic
main() {
    check_git_repo
    
    case "${1:-help}" in
        "validate")
            validate_setup
            ;;
        "status")
            show_status
            ;;
        "trigger")
            if [ -z "$2" ]; then
                print_error "Workflow name required"
                echo "Usage: $0 trigger <workflow> [task]"
                exit 1
            fi
            trigger_workflow "$2" "$3"
            ;;
        "local")
            check_local_env
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@" 