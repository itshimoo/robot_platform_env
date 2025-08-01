# Docker Automation & Pre-built Images

This document explains how to use the automated Docker build system and pre-built images from GitHub Container Registry.

## Overview

The RobotLab platform now supports automated Docker builds that are published to GitHub Container Registry (GHCR). This allows users to pull pre-built images instead of building them locally.

## Available Images

### Image Variants

1. **Base Image** (`:latest`, `:v1.0.0`)
   - Standard ROS Noetic environment
   - Basic development tools
   - No GUI or GPU support

2. **GUI Image** (`:gui-latest`, `:gui-v1.0.0`)
   - Includes X11 support for GUI applications
   - RViz, Gazebo, and other GUI tools
   - Requires X11 forwarding on host

3. **GPU Image** (`:gpu-latest`, `:gpu-v1.0.0`)
   - Includes NVIDIA container toolkit
   - GPU acceleration support
   - Requires NVIDIA Docker runtime

4. **Full Image** (`:full-latest`, `:full-v1.0.0`)
   - Combines GUI and GPU support
   - Complete development environment
   - Best for most use cases

### Image Naming Convention

```
ghcr.io/your-username/robot_platform_env:variant-tag
```

Examples:
- `ghcr.io/your-username/robot_platform_env:latest`
- `ghcr.io/your-username/robot_platform_env:gui-v1.0.0`
- `ghcr.io/your-username/robot_platform_env:gpu-latest`
- `ghcr.io/your-username/robot_platform_env:full-v1.0.0`

## Quick Start

### 1. Pull Pre-built Image

```bash
# Pull the latest full image (recommended)
./scripts/pull-prebuilt.sh latest full

# Or pull specific variant
./scripts/pull-prebuilt.sh v1.0.0 gui
```

### 2. Run Container

```bash
# Basic usage
docker run -it --rm robotlab-ros:latest-full

# With GUI support
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  robotlab-ros:latest-gui

# With GPU support
docker run -it --rm \
  --gpus all \
  robotlab-ros:latest-gpu

# With both GUI and GPU
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --gpus all \
  robotlab-ros:latest-full
```

## Using the Pull Script

The `scripts/pull-prebuilt.sh` script simplifies pulling and using pre-built images:

```bash
# Syntax
./scripts/pull-prebuilt.sh [tag] [variant]

# Examples
./scripts/pull-prebuilt.sh                    # Pull latest base image
./scripts/pull-prebuilt.sh latest             # Pull latest base image
./scripts/pull-prebuilt.sh latest gui         # Pull latest GUI image
./scripts/pull-prebuilt.sh v1.0.0 full       # Pull v1.0.0 full image
./scripts/pull-prebuilt.sh main-sha123 base  # Pull specific commit
```

### Available Variants

- `base` (or `default`) - Standard image
- `gui` - With GUI support
- `gpu` - With GPU support  
- `full` - With both GUI and GPU support

## Manual Docker Pull

You can also pull images directly:

```bash
# Set your repository name
REPO="your-username/robot_platform_env"

# Pull different variants
docker pull ghcr.io/$REPO:latest
docker pull ghcr.io/$REPO:gui-latest
docker pull ghcr.io/$REPO:gpu-latest
docker pull ghcr.io/$REPO:full-latest

# Tag for local use
docker tag ghcr.io/$REPO:full-latest robotlab-ros:latest
```

## GitHub Actions Automation

### Workflow Triggers

The Docker build workflow is triggered by:

1. **Push to main/develop branches** - Builds and publishes images
2. **Git tags** (e.g., `v1.0.0`) - Creates versioned releases
3. **Pull requests** - Builds for testing (not published)
4. **Manual dispatch** - Manual trigger from GitHub UI

### Workflow Features

- **Multi-platform builds** - Supports different architectures
- **Layer caching** - Faster builds using GitHub Actions cache
- **Automatic tagging** - Creates semantic version tags
- **Build variants** - Creates base, GUI, GPU, and full variants
- **Security scanning** - Automated vulnerability scanning

### Viewing Build Status

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Build and Publish Docker Images"
4. View build logs and status

## Configuration

### Environment Variables

Set these in your GitHub repository settings:

- `GITHUB_TOKEN` - Automatically provided
- `DOCKER_USERNAME` - Your Docker Hub username (if using)
- `DOCKER_PASSWORD` - Your Docker Hub password (if using)

### Repository Settings

1. **Packages permissions** - Enable package creation
2. **Actions permissions** - Allow workflow execution
3. **Container registry** - Enable GHCR access

## Troubleshooting

### Common Issues

1. **Image not found**
   ```bash
   # Check if image exists
   docker search ghcr.io/your-username/robot_platform_env
   
   # Verify repository name
   echo $GITHUB_REPOSITORY
   ```

2. **Permission denied**
   ```bash
   # Login to GHCR
   echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin
   ```

3. **Build failures**
   - Check GitHub Actions logs
   - Verify Dockerfile syntax
   - Ensure all dependencies are available

### Local Build Fallback

If pre-built images are unavailable:

```bash
# Build locally
./bin/rx build

# Or build manually
docker build -t robotlab-ros:local .
```

## Advanced Usage

### Custom Image Tags

```bash
# Pull specific version
docker pull ghcr.io/your-username/robot_platform_env:v1.2.3

# Pull development branch
docker pull ghcr.io/your-username/robot_platform_env:develop-sha123

# Pull PR build
docker pull ghcr.io/your-username/robot_platform_env:pr-123
```

### Integration with CI/CD

```yaml
# Example GitHub Actions job
- name: Test with pre-built image
  run: |
    docker pull ghcr.io/${{ github.repository }}:latest
    docker run --rm ghcr.io/${{ github.repository }}:latest \
      bash -c "source /opt/ros/noetic/setup.bash && roscore"
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  robotlab:
    image: ghcr.io/your-username/robot_platform_env:full-latest
    environment:
      - DISPLAY=${DISPLAY}
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix
      - ./workspace:/workspace
    ports:
      - "11311:11311"  # ROS master
      - "8080:8080"    # Web interface
```

## Security

### Image Scanning

- All images are automatically scanned for vulnerabilities
- Security reports are available in GitHub repository
- Critical issues block image publication

### Best Practices

1. **Use specific tags** - Avoid `latest` in production
2. **Scan images** - Regularly check for vulnerabilities
3. **Update regularly** - Pull latest security patches
4. **Verify sources** - Only pull from trusted registries

## Support

For issues with pre-built images:

1. Check GitHub Actions logs
2. Verify repository permissions
3. Test with local build
4. Open an issue in the repository

## Contributing

To contribute to the Docker automation:

1. Fork the repository
2. Make changes to Dockerfile or workflows
3. Test locally with `./bin/rx build`
4. Submit a pull request
5. Ensure CI/CD passes 