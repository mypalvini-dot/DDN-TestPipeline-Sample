"""
SAN Automation Library
A comprehensive library for SAN storage automation and management
"""

from .config import ConfigManager, Config
from .core import BaseSanManager, BaseHostManager, SanAutomationOrchestrator
from .vendors import get_vendor_class, VENDOR_MAP
from .hosts import get_host_class, HOST_MAP
from .utils import setup_logging, get_logger, retry, timeout

__version__ = "1.0.0"
__author__ = "SAN Automation Team"
__all__ = [
    'ConfigManager',
    'Config',
    'BaseSanManager',
    'BaseHostManager',
    'SanAutomationOrchestrator',
    'get_vendor_class',
    'VENDOR_MAP',
    'get_host_class',
    'HOST_MAP',
    'setup_logging',
    'get_logger',
    'retry',
    'timeout'
]
