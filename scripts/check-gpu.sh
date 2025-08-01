#!/bin/bash

# GPU Check Script for RobotLab
# Checks if GPU is available and provides setup instructions

echo "🔍 Checking GPU availability for RobotLab..."
echo "=============================================="

# Check if nvidia-smi is available
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected"
    echo "GPU Information:"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits
    echo ""
    
    # Check if nvidia-docker is available
    if command -v nvidia-docker &> /dev/null; then
        echo "✅ nvidia-docker runtime available"
        echo "🚀 GPU support ready for containers"
    else
        echo "⚠️  nvidia-docker not found"
        echo "💡 Install nvidia-docker for GPU support:"
        echo "   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -"
        echo "   distribution=\$(. /etc/os-release;echo \$ID\$VERSION_ID)"
        echo "   curl -s -L https://nvidia.github.io/nvidia-docker/\$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list"
        echo "   sudo apt-get update && sudo apt-get install -y nvidia-docker2"
        echo "   sudo systemctl restart docker"
    fi
else
    echo "❌ No NVIDIA GPU detected or drivers not installed"
    echo "💡 To enable GPU support:"
    echo "   1. Install NVIDIA drivers: sudo apt install nvidia-driver-xxx"
    echo "   2. Install nvidia-docker: see instructions above"
    echo "   3. Set GPU_ENABLED=true in platform.env"
fi

echo ""
echo "📋 Current GPU configuration:"
if [ -f "platform.env" ]; then
    if grep -q "GPU_ENABLED=true" platform.env; then
        echo "✅ GPU_ENABLED=true in platform.env"
    else
        echo "❌ GPU_ENABLED=false in platform.env"
        echo "💡 Set GPU_ENABLED=true to enable GPU support"
    fi
else
    echo "❌ platform.env not found"
fi

echo ""
echo "🎯 Usage:"
echo "   With GPU:  robocmd run  (when GPU_ENABLED=true)"
echo "   Without GPU: robocmd run (when GPU_ENABLED=false)" 