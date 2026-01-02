"""
Security layer for API key validation

Implements FastAPI dependency for API key authentication.
"""

from fastapi import HTTPException, status
from .config import settings
from .schemas import GenerateRequest


def validate_api_key(request: GenerateRequest) -> bool:
    """
    Validate API key from request body
    
    Args:
        request: GenerateRequest containing the API key
        
    Returns:
        True if valid
        
    Raises:
        HTTPException: 401 Unauthorized if API key is invalid
    """
    if request.api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return True
