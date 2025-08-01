#!/bin/bash
# Pull pre-built Docker images from GitHub Container Registry

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

# Load configuration
if [ -f "platform.env" ]; then
    export $(grep -v '^#' platform.env | xargs)
else
    print_error "platform.env not found"
    exit 1
fi

# Default values
REPO_NAME=${GITHUB_REPOSITORY:-"your-username/robot_platform_env"}
REGISTRY="ghcr.io"
IMAGE_NAME="${REGISTRY}/${REPO_NAME}"
TAG=${1:-"latest"}

# Available image variants
VARIANT=${2:-"base"}

print_status "Pulling pre-built Docker image..."
print_status "Repository: $REPO_NAME"
print_status "Registry: $REGISTRY"
print_status "Image: $IMAGE_NAME"
print_status "Tag: $TAG"
print_status "Variant: $VARIANT"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Determine the full image name based on variant
case $VARIANT in
    "base"|"default")
        FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"
        ;;
    "gui")
        FULL_IMAGE_NAME="${IMAGE_NAME}:gui-${TAG}"
        ;;
    "gpu")
        FULL_IMAGE_NAME="${IMAGE_NAME}:gpu-${TAG}"
        ;;
    "full")
        FULL_IMAGE_NAME="${IMAGE_NAME}:full-${TAG}"
        ;;
    *)
        print_error "Unknown variant: $VARIANT"
        echo "Available variants: base, gui, gpu, full"
        exit 1
        ;;
esac

print_status "Pulling image: $FULL_IMAGE_NAME"

# Pull the image
if docker pull "$FULL_IMAGE_NAME"; then
    print_success "Successfully pulled $FULL_IMAGE_NAME"
    
    # Tag it locally for convenience
    LOCAL_TAG="robotlab-ros:${TAG}-${VARIANT}"
    docker tag "$FULL_IMAGE_NAME" "$LOCAL_TAG"
    print_success "Tagged as: $LOCAL_TAG"
    
    echo ""
    print_status "Usage examples:"
    echo ""
    
    case $VARIANT in
        "base"|"default")
            echo "  # Run basic container"
            echo "  docker run -it --rm $LOCAL_TAG"
            ;;
        "gui")
            echo "  # Run with GUI support"
            echo "  docker run -it --rm \\"
            echo "    -e DISPLAY=\$DISPLAY \\"
            echo "    -v /tmp/.X11-unix:/tmp/.X11-unix \\"
            echo "    $LOCAL_TAG"
            ;;
        "gpu")
            echo "  # Run with GPU support"
            echo "  docker run -it --rm \\"
            echo "    --gpus all \\"
            echo "    $LOCAL_TAG"
            ;;
        "full")
            echo "  # Run with GUI and GPU support"
            echo "  docker run -it --rm \\"
            echo "    -e DISPLAY=\$DISPLAY \\"
            echo "    -v /tmp/.X11-unix:/tmp/.X11-unix \\"
            echo "    --gpus all \\"
            echo "    $LOCAL_TAG"
            ;;
    esac
    
    echo ""
    print_status "Available commands inside container:"
    echo "  • roscore"
    echo "  • rosrun turtlesim turtlesim_node"
    echo "  • rviz"
    echo "  • gazebo"
    echo "  • catkin build"
    
else
    print_error "Failed to pull $FULL_IMAGE_NAME"
    echo ""
    print_warning "This might be because:"
    echo "  1. The image doesn't exist yet (needs to be built first)"
    echo "  2. You don't have access to the repository"
    echo "  3. The repository is private and you need to authenticate"
    echo ""
    print_status "To build locally instead:"
    echo "  ./bin/rx build"
    exit 1
fi 