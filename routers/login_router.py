# -*- coding: utf-8 -*-
import requests
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import traceback

from routers import security_router
from entities.base import Result
from services.database import get_db
from services.config import ConfigService
from services.elogs import ElogsService

router = APIRouter()


@router.get(
    "/login",
    tags=["Login"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="do_login",
)
async def login(
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_config(api_key)

        elog = ElogsService(db)
        response = elog.login(data)

        if response.status_code != 200:
            raise Exception("Error Logging in")

        raw_data = json.loads(response.text)
        token = raw_data["token"]
        expiration = raw_data["expiration"]
        other_urls = elog.get_urls(data["url"], token)
        cfg.update_token(api_key, token, expiration, other_urls.text)
        db.commit()

    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error Logging in",
            "data": [{"msg": str(exc)}],
        }
    return {"status": "OK", "message": "Login successful.", "data": [raw_data]}


@router.get(
    "/user",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_user",
)
async def get_user(
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.get_user(
            data["token"], data["url"], data["other_urls"]["_links"]["user"]["href"]
        )
        return {"status": "OK", "message": "User found.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Getting User",
            "data": [{"msg": str(exc)}],
        }


@router.get(
    "/sites",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_sites",
)
async def get_sites(
    site_name: str | None = None,
    page: int = 1,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.get_sites(
            data["token"],
            data["url"],
            data["other_urls"]["_links"]["user"]["href"],
            data["other_urls"]["_links"]["sites"]["href"],
            site_name,
            page,
        )
        return {"status": "OK", "message": "Sites found.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Getting Sites",
            "data": [{"msg": str(exc)}],
        }


@router.get(
    "/locations",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_locations",
)
async def get_locations(
    site_id: int,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.get_locations(
            data["token"],
            data["url"],
            site_id,
        )
        return {"status": "OK", "message": "Locations found.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Getting Locations",
            "data": [{"msg": str(exc)}],
        }
