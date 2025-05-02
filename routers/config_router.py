# -*- coding: utf-8 -*-

import traceback

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from entities.base import Result, Config, ConfigRefresh, ConfigCreate
from libs.config import JWT_SECRET_KEY, app_cache
from libs.utils import require_admin_api_key
from routers import security_router
from services.config import ConfigService
from services.database import get_db

router = APIRouter()


@router.get(
    "/config",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_config",
)
@require_admin_api_key
async def get_config(
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.list_config()
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Getting Config",
            "data": [{"msg": str(exc)}],
        }
    return {"status": "OK", "message": "Configurations listed.", "data": data}

@router.get(
    "/config/{user_id}",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_config_by_id",
)
@require_admin_api_key
async def get_config_by_id(
        user_id: int,
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)

        # Check if config exists first
        if not cfg.exist_config_by_user_id(user_id):
            return {
                "status": "Error",
                "message": "Configuration not found",
                "data": [{"msg": f"No configuration found for user_id: {user_id}"}],
            }

        # Get the config data
        data = cfg.select_config_by_user_id(user_id)

    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error Getting Config",
            "data": [{"msg": str(exc)}],
        }

    return {
        "status": "OK",
        "message": "Configuration found.",
        "data": [data]
    }

@router.get(
    "/config/token/{user_id}",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_token",
)
@require_admin_api_key
async def get_token(
        user_id: int,
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token_by_user_id(user_id)
    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error getting token",
            "data": [{"msg": str(exc)}],
        }
    return {
        "status": "OK",
        "message": "Token available.",
        "data": [data],
    }


@router.delete(
    "/config/{id}",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="delete_config",
)
@require_admin_api_key
async def delete_config(
        id: int,
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        cfg.delete_config(id)

    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error deleting Configuration",
            "data": [{"msg": str(exc)}],
        }
    return {"status": "OK", "message": "Configuration deleted.", "data": [{"user_id": id}]}


@router.post(
    "/config",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="add_config",
)
@require_admin_api_key
async def add_config(
        request: Request,
        item: ConfigCreate,
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    try:
        # Trim leading and trailing spaces, then remove trailing slash from URL if present
        if item.url:
            item.url = item.url.strip()
            if item.url.endswith('/'):
                item.url = item.url.rstrip('/')

        # Convert ConfigCreate to Config model
        config_obj = Config(
            account_number=item.account_number,
            user_name=item.user_name,
            url=item.url,
            user_pwd=item.user_pwd
        )

        cfg = ConfigService(db)
        config_obj.generate_jwt_api_key(JWT_SECRET_KEY)
        cache_key = f"{config_obj.account_number}-{config_obj.user_name}"
        app_cache[cache_key] = config_obj.user_pwd
        user = request.session.get("user")
        if user:
            config_obj.created_by = user.get('userPrincipalName')
        else:
            config_obj.created_by = "SYSTEM"

        # Get the user_id from the database after adding the config
        user_id = cfg.add_config(config_obj)

        # Return specific fields in response data
        response_data = {
            "api_key": config_obj.api_key,
            "account_number": config_obj.account_number,
            "user_id": user_id,
            "user_name": config_obj.user_name,
            "url": config_obj.url
        }

    except Exception as exc:
        print(traceback.format_exc())
        error_message = str(exc)

        # Check for unique constraint violation for url and user_name
        if "config_url_username_unique" in error_message:
            return {
                "status": "Error",
                "message": "Duplicate configuration",
                "data": [{
                    "msg": f"A configuration for username '{item.user_name}' with URL '{item.url}' already exists. Each combination of username and URL must be unique."}],
            }

        return {
            "status": "Error",
            "message": "Error adding Configuration",
            "data": [{"msg": error_message}],
        }

    return {"status": "OK", "message": "Configuration added.", "data": [response_data]}

@router.post(
    "/config/{user_id}/refresh-credential",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="refresh_config",
)
@require_admin_api_key
async def refresh_credential(
        user_id: int,
        item: ConfigRefresh,
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    """
    Refresh a user's credential (password) in the cache to extend its TTL
    Provide the user_id, password and api_key in the request body for validation
    """
    try:
        # Validate the API key exists in the config table
        cfg = ConfigService(db)
        result = cfg.exist_config_by_user_id(user_id)

        if result:
            data = cfg.select_config_by_user_id(user_id)
            cache_key = f"{data['account_number']}-{data['user_name']}"
            app_cache[cache_key] = item.user_pwd
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Configuration with user id: '{user_id}' not found"
            )
    except Exception as exc:
        print(traceback.format_exc())
        error_message = str(exc)

        return {
            "status": "Error",
            "message": "Error refreshing Configuration",
            "data": [{"msg": error_message}],
        }
    return {"status": "OK", "message": "Configuration refreshed.", "data": []}