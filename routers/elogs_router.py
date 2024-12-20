# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from routers import security_router
from entities.base import ImageData, JobData, Result, JobsBy
from services.database import get_db
from services.config import ConfigService
from services.elogs import ElogsService

router = APIRouter()


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
        user_data = elog.get_locations(data["token"], data["url"], site_id, page)
        return {"status": "OK", "message": "Locations found.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Getting Locations",
            "data": [{"msg": str(exc)}],
        }


@router.get(
    "/tasks",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_tasks",
)
async def get_tasks(
    site_id: int,
    task_id: int | None = None,
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
        if task_id:
            user_data = elog.get_task(data["token"], data["url"], site_id, task_id)
            return {"status": "OK", "message": "Task found.", "data": [user_data]}

        user_data = elog.get_tasks(data["token"], data["url"], site_id, page)
        return {"status": "OK", "message": "Tasks found.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Getting Tasks",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/by",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_jobs_by",
)
async def get_jobs_by(
    jobs_by: JobsBy,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.get_jobs_by(
            data["token"],
            data["url"],
            data["other_urls"]["_links"]["user"]["href"],
            jobs_by,
        )
        return {"status": "OK", "message": "Jobs found.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Getting Jobs",
            "data": [{"msg": str(exc)}],
        }


@router.get(
    "/jobs",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_jobs",
)
async def get_jobs(
    site_id: int,
    job_id: int | None = None,
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
        user_data = elog.get_jobs(data["token"], data["url"], site_id, job_id, page)
        return {"status": "OK", "message": "Jobs found.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Getting Jobs",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/acknowledge",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="acknowledge_job",
)
async def acknowledge_job(
    site_id: int,
    job_id: int,
    job_data: JobData,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.acknowledge_job(
            data["token"], data["url"], site_id, job_id, job_data
        )
        return {"status": "OK", "message": "Job acknowledged.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Acknowledging Job",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/commence",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="commence_job",
)
async def commence_job(
    site_id: int,
    job_id: int,
    job_data: JobData,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.commence_job(
            data["token"], data["url"], site_id, job_id, job_data
        )
        return {"status": "OK", "message": "Job commenced.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Commencing Job",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/complete",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="complete_paperwork_job",
)
async def complete_job(
    site_id: int,
    job_id: int,
    job_data: JobData,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.complete_job(
            data["token"],
            data["url"],
            site_id,
            job_id,
            job_data,
        )
        return {"status": "OK", "message": "Job completed.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Completing Job",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/complete-paperwork",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="complete_job",
)
async def complete_paperwork_job(
    site_id: int,
    job_id: int,
    job_data: JobData,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.complete_paperwork(
            data["token"],
            data["url"],
            site_id,
            job_id,
            job_data,
        )
        return {"status": "OK", "message": "Paperwork completed.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Completing Paperwork",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/create",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="create_job",
)
async def create_job(
    site_id: int,
    job_data: JobData,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.create_job(data["token"], data["url"], site_id, job_data)
        return {"status": "OK", "message": "Job created.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Creating Job",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/approve",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="approve_job",
)
async def approve_job(
    site_id: int,
    job_id: int,
    job_data: JobData,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.approve_job(
            data["token"], data["url"], site_id, job_id, "accept", job_data
        )
        return {"status": "OK", "message": "Job Approved.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Approving Job",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/reject",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="reject_job",
)
async def reject_job(
    site_id: int,
    job_id: int,
    job_data: JobData,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.approve_job(
            data["token"], data["url"], site_id, job_id, "reject", job_data
        )
        return {"status": "OK", "message": "Job Rejected.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Rejecting Job",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/extension/request",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="request_job_extension",
)
async def request_job_extension(
    site_id: int,
    job_id: int,
    job_data: JobData,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.request_job_extension(
            data["token"], data["url"], site_id, job_id, job_data
        )
        return {"status": "OK", "message": "Job Rejected.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Rejecting Job",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/jobs/extension/<status>",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="accept_job_extension",
)
async def accept_job_extension(
    site_id: int,
    job_id: int,
    status: str,
    job_data: JobData,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.accept_job_extension(
            data["token"], data["url"], site_id, job_id, status, job_data
        )
        return {
            "status": "OK",
            "message": f"{status} Job Extension.",
            "data": [user_data],
        }
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Accepting/Rejecting Job Extension",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/files",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="get_file_data",
)
async def get_file_data(
    file_data: dict,
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        user_data = elog.get_file_data(data["token"], data["url"], file_data)
        return {"status": "OK", "message": "File data found.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Getting File Data",
            "data": [{"msg": str(exc)}],
        }


@router.post(
    "/files/upload",
    tags=["ELogs"],
    status_code=status.HTTP_200_OK,
    response_model=Result,
    operation_id="upload_file",
)
async def upload_file(
    key: str = Form(...),
    bucket: str = Form(...),
    construct: str = Form(...),
    google_access_id: str = Form(...),
    content_disposition: str = Form(...),
    policy: str = Form(...),
    signature: str = Form(...),
    success_action_redirect: str = Form(...),
    file_data: UploadFile = File(...),
    api_key: security_router.APIKey = security_router.Depends(
        security_router.get_api_key
    ),
    db: Session = Depends(get_db),
):
    try:
        with open(file_data.filename, "wb") as f:
            f.write(file_data.file.read())

        cfg = ConfigService(db)
        data = cfg.select_token(api_key)
        elog = ElogsService(db)
        image_data = ImageData(
            key=key,
            bucket=bucket,
            google_access_id=google_access_id,
            policy=policy,
            signature=signature,
            content_disposition=content_disposition,
            success_action_redirect=success_action_redirect,
        )
        user_data = elog.upload_file(
            data["token"], image_data, file_data.filename, file_data.content_type
        )
        return {"status": "OK", "message": "File uploaded.", "data": [user_data]}
    except Exception as exc:
        return {
            "status": "Error",
            "message": "Error Uploading File",
            "data": [{"msg": str(exc)}],
        }
