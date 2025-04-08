# -*- coding: utf-8 -*-
from __future__ import annotations

import time
from datetime import datetime
from typing import Literal, Optional

import jwt
from pydantic import BaseModel, Field, field_validator


class Result(BaseModel):
    status: str = Field(title="Status", description="The status of the request")
    message: str = Field(title="Message", description="The message of the request")
    data: list[dict] = Field(title="Data", description="The data of the request")

class ConfigRefresh(BaseModel):
    user_pwd: str = Field(
        title="User Password",
        description="The user password of the ELog api user",
    )

class Config(ConfigRefresh):
    api_key: Optional[str] = Field(
        None,
        title="API Key",
        description="The newly generated API Key",
    )
    account_number: int = Field(
        title="Account Number",
        description="Numeric unique identifier for client organization"
    )
    user_name: str = Field(
        title="User Name", description="The user name of the ELog api user"
    )
    url: str = Field(
        title="Elogs URL",
        description="The url of the ELog api user"
    )
    token: str | None = Field(
        None, title="Token", description="The login token of the ELog api user"
    )
    expiration: int | None = Field(
        None, title="Expiration", description="The date to token expire"
    )
    created_at: int = Field(
        default_factory=lambda: int(time.time()),
        title="Created Date Time",
        description="When this client organization was created"
    )
    created_by: Optional[str] = Field(
        None,  # Default to None to make it optional
        title="Created By",
        description="Username of person who created this client organization"
    )

    @field_validator('url')
    def validate_url(cls, v):
        try:
            from urllib.parse import urlparse
            result = urlparse(v)
            if all([result.scheme, result.netloc]):
                return v
            raise ValueError("Invalid URL format")
        except Exception:
            raise ValueError("Invalid URL format")

    @staticmethod
    def verify_api_key(token: str, secret_key: str) -> dict:
        """
        Verify and decode a JWT token

        Args:
            token: The JWT token to verify
            secret_key: Secret key used to verify the JWT signature

        Returns:
            The decoded payload if verification succeeds

        Raises:
            jwt.InvalidTokenError: If token verification fails
        """
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.InvalidTokenError:
            raise ValueError("Invalid API key")

    def generate_jwt_api_key(self, secret_key: str) -> 'Config':
        """
        Generate a JWT token for this Config instance using the account_number as the key.
        The payload includes only url, created_at, created_by, account_number, user_name,
        and cache_key (<account_number>-<user_name>).

        Args:
            secret_key: Secret key used to sign the JWT

        Returns:
            The updated Config instance with the new JWT API key
        """
        # Generate cache key
        cache_key = f"{self.account_number}-{self.user_name}"

        # Define payload with only the required fields
        payload = {
            "url": self.url,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "account_number": self.account_number,
            "user_name": self.user_name,
            "cache_key": cache_key,
            # Set expiration to a very distant future (effectively "forever")
            "exp": datetime(2099, 12, 31).timestamp()  # Far future expiration
        }

        # Generate JWT
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Update the current instance
        self.api_key = token
        self.expiration = int(datetime(2099, 12, 31).timestamp())  # Same far future expiration

        return self


class JobsBy(BaseModel):
    by: Literal["service provider", "status", "range", "type"] = Field(
        title="By",
        description="The type of the job grouping",
    )
    values: list[str] = Field(title="Values", description="The values of the grouping")


class Jobgroup(BaseModel):
    href: str


class Serviceprovider(BaseModel):
    href: str


class Priority(BaseModel):
    href: str


class _Links(BaseModel):
    jobgroup: Jobgroup
    serviceprovider: Serviceprovider
    priority: Priority


class SiteContact(BaseModel):
    notifyOnCreate: bool
    notifyOnComplete: bool
    declineEmail: bool


class JobData(BaseModel):
    _links: Optional[_Links] = None
    siteContact: Optional[SiteContact] = None
    siteContactSameAsReporter: Optional[bool] = None
    siteContactAvailableOnSite: Optional[bool] = None
    notifyOnCreate: Optional[bool] = None
    notifyOnComplete: Optional[bool] = None
    isOnNextPlannedVisit: Optional[bool] = None
    isByPlannedDate: Optional[bool] = None
    noRequisiteRequired: Optional[bool] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    note: Optional[str] = None
    onSiteDate: Optional[str] = None
    completionDate: Optional[str] = None
    files: Optional[list[str]] = None


class ImageData(BaseModel):
    key: str
    bucket: str
    google_access_id: str
    policy: str
    signature: str
    content_disposition: str
    success_action_redirect: str
