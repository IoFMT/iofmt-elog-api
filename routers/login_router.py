# -*- coding: utf-8 -*-

import json

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import traceback

from libs.config import app_cache
from libs.utils import require_admin_api_key, validate_user_api_key
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
@require_admin_api_key
async def login(
    user_api_key: str,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        validate_user_api_key(user_api_key)

        cfg = ConfigService(db)
        data = cfg.select_config(user_api_key)
        cache_key = f"{data['account_number']}-{data['user_name']}"
        data['user_pwd'] = app_cache.get(cache_key)

        # Check if password is available in the cache
        if data['user_pwd']:
            # Refresh the TTL for this cache entry if it exists
            app_cache[cache_key] = data['user_pwd']
        else:
            return {
                "status": "Error",
                "message": "Authentication Failed",
                "data": [{
                    "msg": f"Password for user '{data['user_name']}' is no longer in memory cache. Please recreate this user configuration."
                }],
            }

        elog = ElogsService(db)
        response = elog.login(data)

        if response.status_code != 200:
            raise Exception("Error Logging in")

        raw_data = json.loads(response.text)
        token = raw_data["token"]
        expiration = raw_data["expiration"]
        other_urls = elog.get_urls(data["url"], token)
        cfg.update_token(user_api_key, token, expiration, other_urls.text)
        db.commit()

    except Exception as exc:
        print(traceback.format_exc())
        return {
            "status": "Error",
            "message": "Error Logging in",
            "data": [{"msg": str(exc)}],
        }
    return {"status": "OK", "message": "Login successful.", "data": [raw_data]}
