import requests
from typing import Dict, List, Optional
from ..config import Config
from .base_vendor import BaseVendor

class GenericVendor(BaseVendor):
    """Generic SAN implementation using REST API"""
    
    def connect(self) -> bool:
        try:
            self.session = requests.Session()
            # Basic authentication
            self.session.auth = (self.config.san_username, self.config.san_password)
            self.session.verify = False  # For self-signed certs
            
            # Test connection
            response = self.session.get(f"{self.api_base_url}/system/info", timeout=10)
            if response.status_code == 200:
                self.connected = True
                return True
            return False
        except Exception as e:
            self._handle_error(f"Connection failed: {e}")
            return False
    
    def disconnect(self) -> bool:
        if self.session:
            self.session.close()
        self.connected = False
        return True
    
    def _api_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        if not self.connected:
            raise ConnectionError("Not connected to SAN")
        
        url = f"{self.api_base_url}{endpoint}"
        response = getattr(self.session, method.lower())(url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def _get_auth_headers(self) -> Dict
