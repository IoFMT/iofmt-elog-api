# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum


class Result(BaseModel):
    status: str = Field(title="Status", description="The status of the request")
    message: str = Field(title="Message", description="The message of the request")
    data: list[dict] = Field(title="Data", description="The data of the request")


class Config(BaseModel):
    api_key: str = Field(
        title="API Key",
        description="The newly generated API Key",
    )
    user_name: str = Field(
        title="User Name", description="The user name of the ELog api user"
    )
    user_pwd: str = Field(
        title="User Password",
        description="The user password of the ELog api user",
    )
    url: str = Field(
        title="URL",
        description="The url of the ELog api user",
    )
    token: str | None = Field(
        None, title="Token", description="The login token of the ELog api user"
    )
    expiration: int | None = Field(
        None, title="Expiration", description="The date to token expire"
    )
