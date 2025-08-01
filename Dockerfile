# RobotLab ROS Dockerfile
# Robot Platform Environment for ROS Development

FROM ros:noetic-ros-core

# Build arguments for conditional features
ARG GUI_ENABLED=false
ARG GPU_ENABLED=false

# Set environment variables
ENV ROS_DISTRO=noetic
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and development tools
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-rosinstall \
    python3-rosinstall-generator \
    python3-wstool \
    python3-catkin-tools \
    python3-rosdep \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    vim \
    nano \
    htop \
    tree \
    tmux \
    # X11 and GUI support (always included for GUI_ENABLED builds)
    x11-apps \
    x11-utils \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxi-dev \
    libxss-dev \
    libxtst-dev \
    && rm -rf /var/lib/apt/lists/*

# Install ROS packages and tools
RUN apt-get update && apt-get install -y \
    ros-noetic-rviz \
    ros-noetic-turtlesim \
    ros-noetic-rqt \
    ros-noetic-rqt-common-plugins \
    ros-noetic-geometry-msgs \
    ros-noetic-std-msgs \
    ros-noetic-sensor-msgs \
    ros-noetic-nav-msgs \
    ros-noetic-tf2 \
    ros-noetic-tf2-ros \
    ros-noetic-tf2-geometry-msgs \
    # Gazebo and simulation packages
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-gazebo-ros-control \
    ros-noetic-gazebo-plugins \
    ros-noetic-gazebo-dev \
    ros-noetic-gazebo-msgs \
    ros-noetic-gazebo-ros \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages for development
RUN pip3 install --upgrade pip && \
    pip3 install \
    numpy \
    scipy \
    matplotlib \
    jupyter \
    ipython \
    rospkg \
    catkin_pkg \
    empy \
    pyyaml \
    defusedxml

# Install GPU support if enabled
RUN if [ "$GPU_ENABLED" = "true" ]; then \
        apt-get update && apt-get install -y \
        nvidia-cuda-toolkit \
        nvidia-driver-470 \
        && rm -rf /var/lib/apt/lists/*; \
    fi

# Initialize rosdep
RUN rosdep init && rosdep update

# Create workspace directory
WORKDIR /workspace

# Initialize ROS workspace
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && \
    mkdir -p src && \
    catkin init"

# Copy entrypoint script
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set up environment
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc && \
    echo "source /workspace/devel/setup.bash" >> ~/.bashrc && \
    echo "export ROS_HOSTNAME=\$(hostname -I | awk '{print \$1}')" >> ~/.bashrc && \
    echo "export ROS_MASTER_URI=http://\$(hostname -I | awk '{print \$1}'):11311" >> ~/.bashrc

# Expose ROS master port
EXPOSE 11311

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"] 