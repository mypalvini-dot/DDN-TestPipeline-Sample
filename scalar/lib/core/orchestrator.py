import time
from typing import Dict, Any
from .base_managers import BaseSanManager, BaseHostManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

class SanAutomationOrchestrator:
    """Orchestrator class to manage the entire automation process"""
    
    def __init__(self, san_manager: BaseSanManager, host_manager: BaseHostManager):
        self.san_manager = san_manager
        self.host_manager = host_manager
        self.operation_status = {
            "san_connection": False,
            "host_connection": False,
            "raid_created": False,
            "volume_created": False,
            "volume_mapped": False,
            "volume_mounted": False,
            "test_completed": False
        }
    
    def initialize_connections(self) -> bool:
        """Initialize connections to SAN and host"""
        logger.info("Initializing connections...")
        
        try:
            # Connect to SAN
            if self.san_manager.connect():
                self.operation_status["san_connection"] = True
                logger.info("SAN connection established")
            else:
                logger.error("Failed to connect to SAN")
                return False
            
            # Connect to host
            if self.host_manager.connect():
                self.operation_status["host_connection"] = True
                logger.info("Host connection established")
            else:
                logger.error("Failed to connect to host")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Connection initialization failed: {e}")
            return False
    
    def create_storage_infrastructure(self) -> bool:
        """Create RAID, volume, and map to host"""
        logger.info("Creating storage infrastructure...")
        
        try:
            # Get available disks
            disks = self.san_manager.get_disks()
            if not disks:
                logger.error("No disks available")
                return False
            
            # Select disks for RAID
            disk_ids = [disk['id'] for disk in disks[:3]]
            logger.info(f"Selected disks for RAID {self.san_manager.config.raid_level}: {disk_ids}")
            
            # Create RAID
            array_id = self.san_manager.create_raid(disk_ids, self.san_manager.config.raid_level)
            if not array_id:
                logger.error("Failed to create RAID array")
                return False
            self.operation_status["raid_created"] = True
            
            # Wait for RAID initialization
            logger.info("Waiting for RAID initialization...")
            time.sleep(30)
            
            # Create volume
            volume_id = self.san_manager.create_volume(
                array_id, 
                self.san_manager.config.volume_name, 
                self.san_manager.config.volume_size_gb
            )
            if not volume_id:
                logger.error("Failed to create volume")
                return False
            self.operation_status["volume_created"] = True
            
            # Map volume to host
            if self.san_manager.map_volume_to_host(volume_id, self.host_manager.config.host_ip):
                self.operation_status["volume_mapped"] = True
                logger.info("Volume mapped to host successfully")
            else:
                logger.error("Failed to map volume to host")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Storage infrastructure creation failed: {e}")
            return False
    
    def configure_host_storage(self) -> bool:
        """Configure storage on host"""
        logger.info("Configuring host storage...")
        
        try:
            # Rescan storage
            if not self.host_manager.rescan_storage():
                logger.error("Failed to rescan storage")
                return False
            
            # Detect new device
            device = self.host_manager.detect_new_device()
            if not device:
                logger.error("No new storage device detected")
                return False
            logger.info(f"Detected new device: {device}")
            
            # Format device
            if not self.host_manager.format_device(device):
                logger.error("Failed to format device")
                return False
            
            # Mount device
            if not self.host_manager.mount_device(device, self.host_manager.config.mount_point):
                logger.error("Failed to mount device")
                return False
            self.operation_status["volume_mounted"] = True
            
            return True
        except Exception as e:
            logger.error(f"Host storage configuration failed: {e}")
            return False
    
    def run_performance_test(self) -> bool:
        """Run performance test"""
        logger.info("Running performance test...")
        
        try:
            result = self.host_manager.run_performance_test(
                self.host_manager.config.mount_point, 
                self.host_manager.config.test_duration
            )
            if result.get('success', False):
                self.operation_status["test_completed"] = True
                logger.info("Performance test completed successfully")
                return True
            else:
                logger.error("Performance test failed")
                return False
        except Exception as e:
            logger.error(f"Performance test failed: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Cleanup resources"""
        logger.info("Cleaning up resources...")
        
        success = True
        
        try:
            # Disconnect from SAN
            if not self.san_manager.disconnect():
                logger.warning("Failed to disconnect from SAN")
                success = False
            
            # Disconnect from host
            if not self.host_manager.disconnect():
                logger.warning("Failed to disconnect from host")
                success = False
            
            return success
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            return False
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get status report of all operations"""
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "operations": self.operation_status,
            "success": all(self.operation_status.values())
        }
