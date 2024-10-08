# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import traceback

from routers import security_router
from entities.base import Result, Config
from services.database import get_db
from services.config import ConfigService

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
        cfg = ConfigService(db)
        data = cfg.list_config()
    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error selecting Configuration",
            "data": [],
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
        cfg = ConfigService(db)
        data = await cfg.select_token(id)
    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error getting token",
            "data": [],
        }
    return {"status": "OK", "message": "Token available.", "data": data}


@router.delete(
    "/config/{id}",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="delete_config",
)
async def delete_config(
    id: int,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = await cfg.delete_config(id)

    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error deleting Configuration",
            "data": [],
        }
    return {"status": "OK", "message": "Configuration deleted.", "data": [id]}


@router.post(
    "/config",
    tags=["Configuration"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="add_config",
)
async def add_config(
    item: Config,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.add_config(item)
    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error adding Configuration",
            "data": [item],
        }

    return {"status": "OK", "message": "Configuration added.", "data": []}
