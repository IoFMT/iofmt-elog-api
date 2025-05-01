# -*- coding: utf-8 -*-
"""Add utility functions here"""

import base64
from functools import wraps

import jwt
from fastapi import HTTPException, status

import libs.config as config
from libs.config import GLOBAL_API_KEY


def encode(value):
    """Generate a base64 encoded string for obsfuscation purposes"""
    return_value = base64.b64encode(value.encode())
    return_value = (
        return_value[2 : len(return_value) - 1]
        + return_value[0:2]
        + return_value[len(return_value) - 1 :]
    )
    return return_value.decode("utf-8")


def decode(value):
    """Decode a base64 encoded string"""
    try:
        encoded = value.encode()
    except:
        encoded = value
    return_value = (
        encoded[len(encoded) - 3 : len(encoded) - 1]
        + encoded[0 : len(encoded) - 3]
        + encoded[len(encoded) - 1 :]
    )
    return_value = base64.b64decode(return_value)
    return return_value.decode()


def require_admin_api_key(func):
    @wraps(func)
    async def wrapper(*args, api_key=None, **kwargs):
        from libs.utils import encode  # Import here to avoid circular imports

        if not api_key or encode(api_key) != GLOBAL_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not allowed. Invalid API key."
            )

        return await func(*args, api_key=api_key, **kwargs)

    return wrapper


def validate_user_api_key(user_api_key: str) -> bool:
    """
    Validate a user API key by checking if it's a valid JWT

    Args:
        user_api_key: The JWT token to verify

    Returns:
        bool: True if the key is valid, False otherwise

    Raises:
        HTTPException: If the key is invalid and should cause a request failure
    """
    if not user_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User API key is required"
        )

    try:
        # Make sure to use the actual secret key from your config
        decoded_jwt = jwt.decode(user_api_key, config.JWT_SECRET_KEY, algorithms=["HS256"])
        return True  # Return True if it's valid
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User API key has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user API key"
        )
