import paramiko
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from ..core.base_managers import BaseHostManager
from ..config import Config

class BaseHost(BaseHostManager, ABC):
    """Base class for host implementations"""
    
    def __init__(self, config: Config):
        super().__init__(config)
        self.ssh_client = None
    
    def connect(self) -> bool:
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                self.config.host_ip,
                username=self.config.host_username,
                password=self.config.host_password,
                timeout=30
            )
            self.connected = True
            return True
        except Exception as e:
            self._handle_error(f"SSH connection failed: {e}")
            return False
    
    def disconnect(self) -> bool:
        if self.ssh_client:
            self.ssh_client.close()
        self.connected = False
        return True
    
    def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute command on host"""
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=timeout)
            return {
                "stdout": stdout.read().decode().strip(),
                "stderr": stderr.read().decode().strip(),
                "exit_code": stdout.channel.recv_exit_status(),
                "success": stdout.channel.recv_exit_status() == 0
            }
        except Exception as e:
            self._handle_error(f"Command execution failed: {e}")
            return {"stdout": "", "stderr": str(e), "exit_code": -1, "success": False}
    
    def _handle_error(self, message: str, exception: Exception = None):
        """Handle errors consistently"""
        from ..utils.logger import get_logger
        logger = get_logger(__name__)
        logger.error(message)
        if exception:
            logger.debug(f"Exception details: {exception}")
