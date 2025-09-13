from .base_host import BaseHost
from .linux_host import LinuxHost
from .windows_host import WindowsHost
from .esxi_host import ESXiHost

__all__ = ['BaseHost', 'LinuxHost', 'WindowsHost', 'ESXiHost']

HOST_MAP = {
    'linux': LinuxHost,
    'windows': WindowsHost,
    'esxi': ESXiHost
}

def get_host_class(host_type: str):
    """Get host class by type"""
    return HOST_MAP.get(host_type.lower(), LinuxHost)
