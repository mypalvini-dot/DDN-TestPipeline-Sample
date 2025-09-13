import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from .schema import ConfigSchema

@dataclass
class Config:
    """Configuration data class"""
    san_ip: str
    host_ip: str
    san_username: str
    san_password: str
    host_username: str
    host_password: str
    raid_level: str = "5"
    volume_size_gb: int = 100
    volume_name: str = "test_volume"
    mount_point: str = "/mnt/san_volume"
    test_duration: int = 300
    vendor_type: str = "generic"
    host_type: str = "linux"
    protocol: str = "iscsi"  # iscsi, fc, nfs, etc.

class ConfigManager:
    """Manage configuration loading, validation, and saving"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.schema = ConfigSchema()
    
    def load_config(self) -> Optional[Config]:
        """Load configuration from file or return defaults"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    validated_data = self.schema.validate(config_data)
                    return Config(**validated_data)
            else:
                return self.get_default_config()
        except Exception as e:
            raise ValueError(f"Failed to load configuration: {e}")
    
    def save_config(self, config: Config) -> bool:
        """Save configuration to file"""
        try:
            config_dict = asdict(config)
            validated_data = self.schema.validate(config_dict)
            
            with open(self.config_file, 'w') as f:
                json.dump(validated_data, f, indent=2)
            return True
        except Exception as e:
            raise ValueError(f"Failed to save configuration: {e}")
    
    def get_default_config(self) -> Config:
        """Return default configuration"""
        return Config(
            san_ip="10.196.172.88",
            host_ip="10.196.172.90",
            san_username="admin",
            san_password="password",
            host_username="root",
            host_password="password"
        )
    
    def update_config(self, **kwargs) -> Config:
        """Update configuration with new values"""
        config = self.load_config()
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config
