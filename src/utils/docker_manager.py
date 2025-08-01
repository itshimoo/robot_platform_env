#!/usr/bin/env python3
"""
Docker Manager for RobotLab
Manages Docker container operations and status monitoring
"""

import os
import subprocess
import json
from typing import Dict, List, Optional
from .config_manager import ConfigManager


class DockerManager:
    """Manages Docker container lifecycle and operations"""
    
    def __init__(self, config: ConfigManager):
        """Initialize the Docker manager"""
        self.config = config
        self.docker_config = config.get_docker_config()
    
    def build_image(self, dockerfile_path: str = "Dockerfile") -> bool:
        """Build Docker image"""
        try:
            image_name = self.docker_config.get('DOCKER_IMAGE_NAME', 'robotlab-ros')
            tag = self.docker_config.get('DOCKER_TAG', 'latest')
            full_image_name = f"{image_name}:{tag}"
            
            print(f"Building Docker image: {full_image_name}")
            print("🚀 Using Docker BuildKit for faster builds...")
            
            # Set BuildKit environment variable for this build
            env = os.environ.copy()
            env['DOCKER_BUILDKIT'] = '1'
            
            cmd = [
                'docker', 'build', 
                '-t', full_image_name,
                '-f', dockerfile_path,
                '.'
            ]
            
            # Run docker build with BuildKit enabled and real-time output
            subprocess.run(cmd, check=True, env=env)
            
            print(f"✅ Successfully built image: {full_image_name}")
            return True
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error building image: {e}")
            return False
        except Exception as e:
            print(f"❌ Exception during build: {e}")
            return False
    
    def run_container(self, port: Optional[int] = None) -> bool:
        """Run Docker container"""
        try:
            container_name = self.docker_config.get('DOCKER_CONTAINER_NAME', 'robotlab-container')
            image_name = self.docker_config.get('DOCKER_IMAGE_NAME', 'robotlab-ros')
            tag = self.docker_config.get('DOCKER_TAG', 'latest')
            full_image_name = f"{image_name}:{tag}"
            
            # Use configured port or default
            if port is None:
                port = self.docker_config.get('DOCKER_PORT', 8080)
            
            # Check if container already exists and remove it
            status = self.get_container_status()
            if (status.get('name') and 
                status.get('name') != 'Unknown'):
                print(f"Container {container_name} already exists. "
                      f"Removing it first...")
                self.remove_container()
            
            print(f"Starting container: {container_name}")
            
            # Set up X11 permissions for GUI applications
            if os.environ.get('DISPLAY'):
                self.setup_x11_permissions()
            
            # Get hostname from config or use container name as fallback
            hostname = self.docker_config.get('CONTAINER_HOSTNAME', 
                                            container_name)
            
            # Check if GPU should be enabled
            gpu_enabled = self.docker_config.get('GPU_ENABLED', False)
            
            # Get current DISPLAY value
            display = os.environ.get('DISPLAY', ':0')
            
            cmd = [
                'docker', 'run',
                '-d',  # detached mode
                '--name', container_name,
                '--hostname', hostname,
                '-p', f"{port}:{port}",
                '-v', f"{os.getcwd()}:{self.docker_config.get('WORKSPACE_PATH', '/workspace')}",
                # X11 forwarding for GUI applications
                '-e', f'DISPLAY={display}',
                '-v', '/tmp/.X11-unix:/tmp/.X11-unix:rw',
                # Additional X11 security settings
                '--security-opt', 'label=type:container_runtime_t',
            ]
            
            # Add GPU support if enabled
            if gpu_enabled:
                print("🚀 GPU support enabled - adding NVIDIA runtime")
                cmd.extend(['--runtime', 'nvidia'])
                cmd.extend(['--gpus', 'all'])
            
            cmd.extend([
                full_image_name,
                'tail', '-f', '/dev/null'  # Keep container running
            ])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Successfully started container: {container_name}")
                return True
            else:
                print(f"Error starting container: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Exception during container start: {e}")
            return False
    
    def stop_container(self) -> bool:
        """Stop Docker container"""
        try:
            container_name = self.docker_config.get('DOCKER_CONTAINER_NAME', 'robotlab-container')
            
            print(f"Stopping container: {container_name}")
            
            cmd = ['docker', 'stop', container_name]
            
            # Run docker stop with real-time output
            subprocess.run(cmd, check=True)
            
            print(f"✅ Successfully stopped container: {container_name}")
            return True
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error stopping container: {e}")
            return False
        except Exception as e:
            print(f"❌ Exception during container stop: {e}")
            return False
    
    def remove_container(self) -> bool:
        """Remove Docker container"""
        try:
            container_name = self.docker_config.get('DOCKER_CONTAINER_NAME', 'robotlab-container')
            
            print(f"Removing container: {container_name}")
            
            cmd = ['docker', 'rm', container_name]
            
            # Run docker rm with real-time output
            subprocess.run(cmd, check=True)
            
            print(f"✅ Successfully removed container: {container_name}")
            return True
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error removing container: {e}")
            return False
        except Exception as e:
            print(f"❌ Exception during container removal: {e}")
            return False
    
    def get_container_status(self) -> Dict[str, any]:
        """Get container status information"""
        try:
            container_name = self.docker_config.get('DOCKER_CONTAINER_NAME', 'robotlab-container')
            
            cmd = [
                'docker', 'ps', 
                '-a', 
                '--filter', f"name={container_name}",
                '--format', 'json'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                # Parse the JSON output
                container_info = json.loads(result.stdout.strip())
                
                return {
                    'name': container_info.get('Names', ''),
                    'status': container_info.get('Status', ''),
                    'ports': container_info.get('Ports', ''),
                    'image': container_info.get('Image', ''),
                    'running': container_info.get('Status', '').startswith('Up'),
                    'created': container_info.get('CreatedAt', '')
                }
            else:
                return {
                    'name': container_name,
                    'status': 'Not found',
                    'ports': '',
                    'image': '',
                    'running': False,
                    'created': ''
                }
                
        except Exception as e:
            print(f"Exception getting container status: {e}")
            return {
                'name': 'Unknown',
                'status': 'Error',
                'ports': '',
                'image': '',
                'running': False,
                'created': ''
            }
    
    def shell_into_container(self) -> bool:
        """Shell into running container"""
        try:
            container_name = self.docker_config.get('DOCKER_CONTAINER_NAME', 'robotlab-container')
            
            cmd = [
                'docker', 'exec', '-it',
                container_name,
                'bash'
            ]
            
            # Use subprocess.Popen to keep the shell interactive
            process = subprocess.Popen(cmd)
            process.wait()
            
            return True
                
        except Exception as e:
            print(f"Error shelling into container: {e}")
            return False
    
    def get_logs(self, lines: int = 50) -> str:
        """Get container logs"""
        try:
            container_name = self.docker_config.get('DOCKER_CONTAINER_NAME', 'robotlab-container')
            
            cmd = [
                'docker', 'logs',
                '--tail', str(lines),
                container_name
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout
            else:
                return result.stderr
                
        except Exception as e:
            return f"Error getting logs: {e}"
    
    def list_images(self) -> List[Dict[str, str]]:
        """List available Docker images"""
        try:
            cmd = [
                'docker', 'images',
                '--format', 'json'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                images = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        images.append(json.loads(line))
                return images
            else:
                return []
                
        except Exception as e:
            print(f"Exception listing images: {e}")
            return []
    
    def cleanup_images(self) -> bool:
        """Clean up unused Docker images"""
        try:
            print("Cleaning up unused Docker images...")
            
            cmd = ['docker', 'image', 'prune', '-f']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Successfully cleaned up unused images")
                return True
            else:
                print(f"Error cleaning up images: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Exception during cleanup: {e}")
            return False
    
    def is_docker_running(self) -> bool:
        """Check if Docker daemon is running"""
        try:
            cmd = ['docker', 'info']
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def setup_x11_permissions(self) -> bool:
        """Set up X11 permissions for GUI applications"""
        try:
            # Allow local connections to X server
            subprocess.run(['xhost', '+local:'], check=True)
            print("🔓 X11 permissions configured")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to set X11 permissions: {e}")
            return False
        except FileNotFoundError:
            print("❌ xhost command not found. X11 may not be available.")
            return False
    
    def pull_image(self, image_name: Optional[str] = None, tag: Optional[str] = None) -> bool:
        """Pull Docker image from registry"""
        try:
            # Use configured values if not provided
            if image_name is None:
                image_name = self.docker_config.get('DOCKER_IMAGE_NAME', 'robotlab-ros')
            if tag is None:
                tag = self.docker_config.get('DOCKER_TAG', 'latest')
            
            full_image_name = f"{image_name}:{tag}"
            
            print(f"🔄 Pulling Docker image: {full_image_name}")
            print("📥 Downloading latest version from registry...")
            
            cmd = ['docker', 'pull', full_image_name]
            
            # Run docker pull with real-time output
            subprocess.run(cmd, check=True)
            
            print(f"✅ Successfully pulled image: {full_image_name}")
            return True
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error pulling image: {e}")
            return False
        except Exception as e:
            print(f"❌ Exception during pull: {e}")
            return False


def main():
    """Test the Docker manager"""
    config = ConfigManager()
    docker_mgr = DockerManager(config)
    
    print("Docker status:")
    print(f"  Docker running: {docker_mgr.is_docker_running()}")
    
    print("\nContainer status:")
    status = docker_mgr.get_container_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\nAvailable images:")
    images = docker_mgr.list_images()
    for image in images[:5]:  # Show first 5 images
        print(f"  {image.get('Repository', 'Unknown')}:{image.get('Tag', 'Unknown')}")


if __name__ == "__main__":
    main() 