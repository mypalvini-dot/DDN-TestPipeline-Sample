from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from ..core.base_managers import BaseSanManager
from ..config import Config

class BaseVendor(BaseSanManager, ABC):
    """Base class for vendor-specific SAN implementations"""
    
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_base_url = f"https://{config.san_ip}/api"
        self.session = None
    
    @abstractmethod
    def _api_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make API request to SAN"""
        pass
    
    @abstractmethod
    def _get_auth_headers(self) -> Dict:
        """Get authentication headers"""
        pass
    
    def get_disks(self) -> Optional[List[Dict]]:
        """Get available disks - default implementation"""
        try:
            response = self._api_request('GET', '/storage/disks')
            return response.get('disks', [])
        except Exception as e:
            self._handle_error(f"Failed to get disks: {e}")
            return None
    
    def _handle_error(self, message: str, exception: Exception = None):
        """Handle errors consistently"""
        from ..utils.logger import get_logger
        logger = get_logger(__name__)
        logger.error(message)
        if exception:
            logger.debug(f"Exception details: {exception}")
