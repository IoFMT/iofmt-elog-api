# -*- coding: utf-8 -*-
import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKey, APIKeyCookie, APIKeyHeader, APIKeyQuery
from starlette.status import HTTP_403_FORBIDDEN


from sqlalchemy.orm import Session

import libs.config as config
from libs.utils import encode
from services.database import get_db

API_KEY = None
API_KEY_NAME = "X-Access-Token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


def retrieve_api_key(api_key: str, db: Session):
    if encode(api_key) == config.GLOBAL_API_KEY:
        return api_key
    else:
        return None

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
    db: Session = Depends(get_db),
):
    if api_key_query:
        results = retrieve_api_key(api_key_query, db)
        if results:
            return api_key_query
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
            )
    elif api_key_header:
        results = retrieve_api_key(api_key_header, db)
        if results:
            return api_key_header
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
            )
    elif api_key_cookie:
        results = retrieve_api_key(api_key_cookie, db)
        if results:
            return api_key_cookie
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
            )
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
