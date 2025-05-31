import subprocess
import time
import logging
import requests
import os
from zapv2 import ZAPv2

logger = logging.getLogger(__name__)

class DockerZAPRunner:
    """OWASP ZAP running in Docker container"""
    
    def __init__(self):
        self.container_name = "vortiqx-zap"
        self.zap_port = 8080
        self.zap_host = "127.0.0.1"
        self.api_key = self._generate_api_key()
        self.zap = None
        
    def _generate_api_key(self):
        """Generate a simple API key for ZAP"""
        import secrets
        return secrets.token_hex(16)
    
    def start_zap_container(self):
        """Start OWASP ZAP in a Docker container"""
        try:
            # Check if container is already running
            result = subprocess.run(
                ["docker", "ps", "-q", "-f", f"name={self.container_name}"],
                capture_output=True, text=True
            )
            
            if result.stdout.strip():
                logger.info("ZAP container is already running")
                return True
                
            # Stop and remove existing container if it exists
            subprocess.run(
                ["docker", "stop", self.container_name],
                capture_output=True, text=True
            )
            subprocess.run(
                ["docker", "rm", self.container_name],
                capture_output=True, text=True
            )
            
            # Start new ZAP container
            cmd = [
                "docker", "run", "-d",
                "--name", self.container_name,
                "-p", f"{self.zap_port}:8080",
                "-i", "owasp/zap2docker-stable",
                "zap.sh", "-daemon",
                "-host", "0.0.0.0",
                "-port", "8080",
                "-config", f"api.key={self.api_key}",
                "-config", "api.addrs.addr.name=.*",
                "-config", "api.addrs.addr.regex=true"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Failed to start ZAP container: {result.stderr}")
                return False
                
            # Wait for ZAP to start
            logger.info("Starting ZAP container, waiting for it to be ready...")
            for i in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get(f"http://{self.zap_host}:{self.zap_port}")
                    if response.status_code == 200:
                        logger.info("ZAP container is ready")
                        return True
                except:
                    pass
                time.sleep(1)
            
            logger.error("ZAP container failed to start within timeout")
            return False
            
        except FileNotFoundError:
            logger.error("Docker is not installed or not available")
            return False
        except Exception as e:
            logger.error(f"Error starting ZAP container: {str(e)}")
            return False
    
    def stop_zap_container(self):
        """Stop the ZAP container"""
        try:
            subprocess.run(
                ["docker", "stop", self.container_name],
                capture_output=True, text=True
            )
            subprocess.run(
                ["docker", "rm", self.container_name],
                capture_output=True, text=True
            )
            logger.info("ZAP container stopped")
        except Exception as e:
            logger.error(f"Error stopping ZAP container: {str(e)}")
    
    def get_zap_client(self):
        """Get ZAP API client"""
        if not self.zap:
            self.zap = ZAPv2(
                proxies={
                    'http': f'http://{self.zap_host}:{self.zap_port}',
                    'https': f'http://{self.zap_host}:{self.zap_port}'
                },
                apikey=self.api_key
            )
        return self.zap
    
    def is_zap_available(self):
        """Check if ZAP is running and accessible"""
        try:
            zap = self.get_zap_client()
            version = zap.core.version
            logger.info(f"ZAP is available. Version: {version}")
            return True
        except Exception as e:
            logger.error(f"ZAP is not available: {str(e)}")
            return False
    
    def ensure_zap_running(self):
        """Ensure ZAP is running, start if needed"""
        if self.is_zap_available():
            return True
            
        logger.info("ZAP not available, attempting to start...")
        if self.start_zap_container():
            # Wait a bit more for ZAP to fully initialize
            time.sleep(5)
            return self.is_zap_available()
        
        return False