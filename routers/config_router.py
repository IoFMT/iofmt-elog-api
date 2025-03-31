# -*- coding: utf-8 -*-

import traceback

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.requests import Request

from entities.base import Result, Config
from libs.config import GLOBAL_API_KEY, JWT_SECRET_KEY, app_cache
from libs.utils import encode
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
async def get_config(
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    try:
        if encode(api_key) != GLOBAL_API_KEY:
            raise Exception("Operation Not allowed.")

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
    "/config/token/{id}",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_token",
)
async def get_token(
        id: str,
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    try:
        if encode(api_key) != GLOBAL_API_KEY:
            raise Exception("Operation Not allowed.")

        cfg = ConfigService(db)
        data = cfg.select_token(id)
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
async def delete_config(
        id: str,
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    try:
        if encode(api_key) != GLOBAL_API_KEY:
            raise Exception("Operation Not allowed.")

        cfg = ConfigService(db)
        data = cfg.delete_config(id)

    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error deleting Configuration",
            "data": [{"msg": str(exc)}],
        }
    return {"status": "OK", "message": "Configuration deleted.", "data": [{"id": id}]}


@router.post(
    "/config",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="add_config",
)
async def add_config(
        request: Request,
        item: Config,
        api_key: security_router.APIKey = security_router.Depends(
            security_router.get_api_key
        ),
        db: Session = Depends(get_db),
):
    try:
        if encode(api_key) != GLOBAL_API_KEY:
            raise Exception("Operation Not allowed.")

        cfg = ConfigService(db)
        item.generate_jwt_api_key(JWT_SECRET_KEY)
        cache_key = f"{item.account_number}-{item.user_name}"
        app_cache[cache_key] = item.user_pwd
        user = request.session.get("user")
        item.created_by = user.get('userPrincipalName')
        cfg.add_config(item)
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

    return {"status": "OK", "message": "Configuration added.", "data": []}
