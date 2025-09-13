import re
from typing import Dict, Optional, Any
from .base_host import BaseHost

class LinuxHost(BaseHost):
    """Linux host implementation"""
    
    def rescan_storage(self) -> bool:
        try:
            # Rescan SCSI bus
            commands = [
                "for host in /sys/class/scsi_host/host*/scan; do echo '- - -' > $host; done",
                "echo 1 > /sys/class/fc_host/host*/issue_lip",
                "rescan-scsi-bus.sh"  # If available
            ]
            
            for cmd in commands:
                result = self.execute_command(cmd)
                if not result['success']:
                    continue  # Try next command
            
            return True
        except Exception as e:
            self._handle_error(f"Storage rescan failed: {e}")
            return False
    
    def detect_new_device(self) -> Optional[str]:
        try:
            # Get block devices
            result = self.execute_command("lsblk -d -o NAME,SIZE,MODEL,TYPE | grep -E '^(sd|nvme)'")
            devices = result['stdout'].splitlines()
            
            # Look for new devices (simplified logic)
            for device in devices:
                if 'LUN' in device or 'VOLUME' in device:
                    parts = device.split()
                    if parts:
                        return f"/dev/{parts[0]}"
            
            # Fallback to checking /dev/sdX devices
            result = self.execute_command("ls /dev/sd* | grep -E '/dev/sd[b-z]'")
            if result['success'] and result['stdout']:
                return result['stdout'].split()[0]
            
            return None
        except Exception as e:
            self._handle_error(f"Device detection failed: {e}")
            return None
    
    def format_device(self, device: str, filesystem: str = "ext4") -> bool:
        try:
            # Unmount if mounted
            self.execute_command(f"umount {device} 2>/dev/null")
            
            # Create filesystem
            cmd = f"mkfs.{filesystem} {device}"
            result = self.execute_command(cmd, timeout=120)
            return result['success']
        except Exception as e:
            self._handle_error(f"Format failed: {e}")
            return False
    
    def mount_device(self, device: str, mount_point: str) -> bool:
        try:
            # Create mount point
            self.execute_command(f"mkdir -p {mount_point}")
            
            # Mount device
            result = self.execute_command(f"mount {device} {mount_point}")
            return result['success']
        except Exception as e:
            self._handle_error(f"Mount failed: {e}")
            return False
    
    def run_performance_test(self, mount_point: str, duration: int) -> Dict[str, Any]:
        try:
            # Use fio for performance testing
            fio_config = f"""
            [global]
            ioengine=libaio
            direct=1
            runtime={duration}
            time_based
            group_reporting
            
            [read_test]
            rw=randread
            bs=4k
            iodepth=32
            size=1G
            directory={mount_point}
            
            [write_test]
            rw=randwrite
            bs=4k
            iodepth=32
            size=1G
            directory={mount_point}
            """
            
            # Write config and run fio
            self.execute_command(f"echo '{fio_config}' > {mount_point}/fio_config.ini")
            result = self.execute_command(f"fio {mount_point}/fio_config.ini --output-format=json", timeout=duration + 60)
            
            return {
                "success": result['success'],
                "output": result['stdout'],
                "error": result['stderr']
            }
        except Exception as e:
            self._handle_error(f"Performance test failed: {e}")
            return {"success": False, "error": str(e)}
