import re
from typing import Tuple

def validate_ip(ip_address: str) -> bool:
    """Validate IP address format"""
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return bool(re.match(pattern, ip_address))

def validate_credentials(username: str, password: str) -> Tuple[bool, str]:
    """Validate credentials"""
    if not username or not password:
        return False, "Username and password cannot be empty"
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Credentials are valid"
