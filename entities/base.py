# -*- coding: utf-8 -*-
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal, Optional
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
