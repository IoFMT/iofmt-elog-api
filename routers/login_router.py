# -*- coding: utf-8 -*-

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import traceback

from routers import security_router
from entities.base import Result, JobsBy
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
