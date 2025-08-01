#!/usr/bin/env python3
"""
Configuration Manager for RobotLab
Handles environment configuration and Docker file generation
"""

import os
from typing import Dict, Any


class ConfigManager:
    """Manages configuration loading, parsing, and Docker file generation"""
    
    def __init__(self, config_file: str = "platform.env"):
        """Initialize the configuration manager"""
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        # Load robot configuration from .env file
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from platform.env file"""
        if not os.path.exists(self.config_file):
            print(f"Warning: Configuration file {self.config_file} not found")
            return
        
        try:
            with open(self.config_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key=value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if ((value.startswith('"') and value.endswith('"')) or 
                            (value.startswith("'") and value.endswith("'"))):
                            value = value[1:-1]
                        
                        # Convert boolean values
                        if value.lower() in ['true', 'false']:
                            self.config[key] = value.lower() == 'true'
                        
                        # Convert numeric values
                        elif value.isdigit():
                            self.config[key] = int(value)
                        elif (value.replace('.', '').isdigit() and 
                              value.count('.') == 1):
                            self.config[key] = float(value)
                        else:
                            self.config[key] = value
                        
        except Exception as e:
            print(f"Error loading configuration: {e}")
    
    def reload_config(self) -> None:
        """Reload configuration from platform.env file"""
        # Clear existing config
        self.config.clear()
        # Reload from file
        self.load_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self.config.copy()
    
    def save_config(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                for key, value in self.config.items():
                    if isinstance(value, str) and ' ' in value:
                        f.write(f'{key}="{value}"\n')
                    else:
                        f.write(f'{key}={value}\n')
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def generate_dockerfile(self, template_path: str = "templates/Dockerfile.template") -> str:
        """Generate Dockerfile from template"""
        if not os.path.exists(template_path):
            return self._generate_default_dockerfile()
        
        try:
            with open(template_path, 'r') as f:
                template = f.read()
            
            # Replace placeholders with configuration values
            dockerfile = template
            for key, value in self.config.items():
                placeholder = f"${{{key}}}"
                if placeholder in dockerfile:
                    dockerfile = dockerfile.replace(placeholder, str(value))
            
            return dockerfile
            
        except Exception as e:
            print(f"Error generating Dockerfile: {e}")
            return self._generate_default_dockerfile()
    
    def _generate_default_dockerfile(self) -> str:
        """Generate default Dockerfile if template not found"""
        ros_distro = self.get('ROS_DISTRO', 'noetic')
        ros_version = self.get('ROS_VERSION', '1.15.15')
        python_version = self.get('ROS_PYTHON_VERSION', '3')
        
        dockerfile = f"""# RobotLab ROS Dockerfile
FROM ros:{ros_distro}-ros-core

# Set environment variables
ENV ROS_DISTRO={ros_distro}
ENV ROS_VERSION={ros_version}
ENV PYTHON_VERSION={python_version}

# Install additional packages
RUN apt-get update && apt-get install -y \\
    python{python_version}-pip \\
    python{python_version}-rosinstall \\
    python{python_version}-rosinstall-generator \\
    python{python_version}-wstool \\
    python{python_version}-catkin-tools \\
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /workspace

# Initialize ROS workspace
RUN /bin/bash -c "source /opt/ros/{ros_distro}/setup.bash && \\
    mkdir -p src && \\
    catkin init"

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
"""
        return dockerfile
    
    def validate_config(self) -> bool:
        """Validate configuration values"""
        required_keys = [
            'PROJECT_NAME',
            'DOCKER_IMAGE_NAME',
            'DOCKER_CONTAINER_NAME',
            'ROS_DISTRO'
        ]
        
        missing_keys = [key for key in required_keys if key not in self.config]
        
        if missing_keys:
            print(f"Missing required configuration keys: {missing_keys}")
            return False
        
        return True
    
    def get_docker_config(self) -> Dict[str, Any]:
        """Get Docker-specific configuration"""
        docker_config = {}
        docker_keys = [
            'DOCKER_IMAGE_NAME',
            'DOCKER_CONTAINER_NAME',
            'DOCKER_TAG',
            'DOCKER_PORT',
            'DOCKER_VOLUME_PATH',
            'GPU_ENABLED'
        ]
        
        for key in docker_keys:
            if key in self.config:
                docker_config[key] = self.config[key]
        
        return docker_config
    
    def get_ros_config(self) -> Dict[str, Any]:
        """Get ROS-specific configuration"""
        ros_config = {}
        ros_keys = [
            'ROS_DISTRO',
            'ROS_VERSION',
            'ROS_PYTHON_VERSION'
        ]
        
        for key in ros_keys:
            if key in self.config:
                ros_config[key] = self.config[key]
        
        return ros_config


def main():
    """Test the configuration manager"""
    config = ConfigManager()
    
    print("Configuration loaded:")
    for key, value in config.get_all().items():
        print(f"  {key}: {value}")
    
    print("\nDocker configuration:")
    for key, value in config.get_docker_config().items():
        print(f"  {key}: {value}")
    
    print("\nROS configuration:")
    for key, value in config.get_ros_config().items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main() 