class SanError(Exception):
    """Base exception for SAN-related errors"""
    pass

class HostError(Exception):
    """Base exception for host-related errors"""
    pass

class ConfigError(Exception):
    """Base exception for configuration errors"""
    pass

class ConnectionError(SanError, HostError):
    """Connection-related errors"""
    pass

class OperationError(SanError):
    """SAN operation errors"""
    pass

class AuthenticationError(ConnectionError):
    """Authentication errors"""
    pass
