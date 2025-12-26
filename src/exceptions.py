"""
Custom exceptions for the Feature Flag Manager API
"""


class ValidationError(Exception):
    """Raised when input validation fails"""
    pass


class ParameterStoreError(Exception):
    """Raised when AWS Parameter Store operations fail"""
    pass


class ParameterNotFoundError(ParameterStoreError):
    """Raised when a parameter is not found"""
    pass
