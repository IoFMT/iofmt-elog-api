# -*- coding: utf-8 -*-
"""
    Main file to run the API
"""
from functools import wraps
import secrets
import traceback

from time import time
from typing import Any


import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from entities.base import Result
from routers import config_router, elogs_router, login_router, azure_auth

from libs import config
from libs.utils import decode, encode

app = FastAPI(title="IoFMT ELog Wrapper REST API", version="0.1.0")
templates = Jinja2Templates(directory="static")

# -------------------------------------------------
# Adding Routers
# -------------------------------------------------
app.include_router(config_router.router)
app.include_router(login_router.router)
app.include_router(elogs_router.router)
app.include_router(azure_auth.router)


# -------------------------------------------------
# Adding Middlewares
# -------------------------------------------------
app.add_middleware(SessionMiddleware, secret_key=config.AZAD_SESSION_SECRET)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def time_call(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time()
    response.headers["X-Process-Time"] = str(process_time - start_time)
    return response


def rate_limited(max_calls: int, time_frame: int):
    """
    :param max_calls: Maximum number of calls allowed in the specified time frame.
    :param time_frame: The time frame (in seconds) for which the limit applies.
    :return: Decorator function.
    """

    def decorator(func):
        calls = []

        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time()
            calls_in_time_frame = [call for call in calls if call > now - time_frame]
            if len(calls_in_time_frame) >= max_calls:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded.",
                )
            calls.append(now)
            return await func(*args, **kwargs)

        return wrapper

    return decorator


# -------------------------------------------------
# Customizing OpenAPI definition
# We need to downgrade to 3.0.2 to be compatible
# with Power Platform Custom Connector
# -------------------------------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="IoFMT ELog Wrapper REST API",
        version="0.1.0",
        summary="This is a wrapper REST API for ELog project",
        description="""This REST API acts as a wrapper to interact with the ELog API.
        <br><br>
        This API is also mapped in a Power Platform Custom Connector.
        <br><br>
        To generate the API KEY for a customer, please go to: <a href='/admin' target='_blank'>Admin</a>""",
        routes=app.routes,
        openapi_version="3.0.2",
        tags=config.tags_metadata,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# -------------------------------------------------
# Endpoints
# -------------------------------------------------
@app.get("/", tags=["Basic"], response_model=Result, operation_id="get_api_status")
async def get_api_status() -> Any:
    return {
        "status": "OK",
        "message": "IoFMT Elogs REST API is running",
        "data": [{"version": "0.1.0"}],
    }


@app.get("/admin", tags=["Basic"], response_class=HTMLResponse, include_in_schema=False)
@rate_limited(config.THROTTLE_RATE, config.THROTTLE_TIME)
async def admin(request: Request) -> Any:
    """Protected admin page."""
    user = request.session.get("user")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "name": user.get("displayName") if user else None,
            "master_api_key": decode(config.GLOBAL_API_KEY)
        },
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
