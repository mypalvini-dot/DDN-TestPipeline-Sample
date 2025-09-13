from typing import Dict, Any
import re

class ConfigSchema:
    """Configuration validation schema"""
    
    def validate(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration data"""
        validated = config_data.copy()
        
        # Validate IP addresses
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if not re.match(ip_pattern, validated.get('san_ip', '')):
            raise ValueError("Invalid SAN IP address")
        if not re.match(ip_pattern, validated.get('host_ip', '')):
            raise ValueError("Invalid host IP address")
        
        # Validate RAID level
        valid_raid_levels = ['0', '1', '5', '6', '10']
        if validated.get('raid_level') not in valid_raid_levels:
            raise ValueError(f"Invalid RAID level. Must be one of: {valid_raid_levels}")
        
        # Validate sizes
        if validated.get('volume_size_gb', 0) <= 0:
            raise ValueError("Volume size must be positive")
        if validated.get('test_duration', 0) <= 0:
            raise ValueError("Test duration must be positive")
        
        return validated
