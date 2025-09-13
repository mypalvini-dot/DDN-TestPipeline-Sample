from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from ..config import Config

class BaseSanManager(ABC):
    """Abstract base class for SAN storage management"""
    
    def __init__(self, config: Config):
        self.config = config
        self.connected = False
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to SAN device"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from SAN device"""
        pass
    
    @abstractmethod
    def get_disks(self) -> Optional[List[Dict]]:
        """Get available disks"""
        pass
    
    @abstractmethod
    def create_raid(self, disk_ids: List[str], raid_level: str) -> Optional[str]:
        """Create RAID array"""
        pass
    
    @abstractmethod
    def create_volume(self, array_id: str, name: str, size_gb: int) -> Optional[str]:
        """Create volume on RAID array"""
        pass
    
    @abstractmethod
    def map_volume_to_host(self, volume_id: str, host_identifier: str) -> bool:
        """Map volume to host"""
        pass

class BaseHostManager(ABC):
    """Abstract base class for host management"""
    
    def __init__(self, config: Config):
        self.config = config
        self.connected = False
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to host"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from host"""
        pass
    
    @abstractmethod
    def rescan_storage(self) -> bool:
        """Rescan storage devices"""
        pass
    
    @abstractmethod
    def detect_new_device(self) -> Optional[str]:
        """Detect new storage device"""
        pass
    
    @abstractmethod
    def format_device(self, device: str, filesystem: str = "ext4") -> bool:
        """Format storage device"""
        pass
    
    @abstractmethod
    def mount_device(self, device: str, mount_point: str) -> bool:
        """Mount storage device"""
        pass
    
    @abstractmethod
    def run_performance_test(self, mount_point: str, duration: int) -> Dict[str, Any]:
        """Run storage performance test"""
        pass
