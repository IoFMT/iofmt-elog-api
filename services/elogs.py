# -*- coding: utf-8 -*-

import json
import traceback
import requests

from sqlalchemy import text


from libs import config
from entities.base import Config


class ElogsService:
    db = None

    def __init__(self, db):
        self.db = db

    def login(self, data):
        try:
            url = data["url"] + "/auth"
            payload = {"username": data["user_name"], "password": data["user_pwd"]}
            files = []
            headers = {
                "Content-Type": "application/json",
            }

            response = requests.request(
                "POST", url, headers=headers, json=payload, files=files
            )
            return response
        except Exception as exc:
            raise Exception("Error Accessing ELog API")

    def get_urls(self, base_url, token):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            response = requests.request("GET", base_url, headers=headers)
            return response
        except Exception as exc:
            raise Exception("Error Accessing ELog API - Not able to get URLs")

    def get_user(self, token, base_url, url):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            user_url = f"{base_url}/{url}"
            response = requests.request("GET", user_url, headers=headers)
            return json.loads(response.text)
        except Exception as exc:
            raise Exception("Error Accessing ELog API - Not able to get User")

    def get_sites(self, token, base_url, user_url, site_url, site_name=None, page=1):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = f"{base_url}/{user_url}/{site_url}?page={page}{'&siteName=' + site_name if site_name else ''}"
            response = requests.request("GET", final_url, headers=headers)
            return json.loads(response.text)
        except Exception as exc:
            raise Exception("Error Accessing ELog API - Not able to get Sites")

    def get_locations(self, token, base_url, site_id, page=1):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = f"{base_url}/sites/{site_id}/locations?page={page}"
            response = requests.request("GET", final_url, headers=headers)
            return json.loads(response.text)
        except Exception as exc:
            raise Exception("Error Accessing ELog API - Not able to get Locations")

    def get_tasks(self, token, base_url, site_id, page=1):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = f"{base_url}/sites/{site_id}/tasks?page={page}"
            response = requests.request("GET", final_url, headers=headers)
            return json.loads(response.text)
        except Exception as exc:
            raise Exception("Error Accessing ELog API - Not able to get Tasks")

    def get_task(self, token, base_url, site_id, task_id):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = f"{base_url}/sites/{site_id}/tasks/{task_id}"
            response = requests.request("GET", final_url, headers=headers)
            return json.loads(response.text)
        except Exception as exc:
            raise Exception("Error Accessing ELog API - Not able to get Task")

    def get_jobs_by(self, token, base_url, user_url, jobs_by):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = None
            if jobs_by.by == "service provider":
                final_url = (
                    f"{base_url}/{user_url}/jobs?serviceProvider={jobs_by.values[0]}"
                )
            elif jobs_by.by == "status":
                final_url = f"{base_url}/{user_url}/jobs?{'&'.join(['status[]='+x for x in jobs_by.values])}"
            elif jobs_by.by == "range":
                final_url = f"{base_url}/{user_url}/jobs?createdAtStart={jobs_by.values[0]}&createdAtEnd={jobs_by.values[1]}"
            elif jobs_by.by == "type":
                final_url = f"{base_url}/{user_url}/jobs?type={jobs_by.values[0]}"
            response = requests.request("GET", final_url, headers=headers)
            return json.loads(response.text)
        except Exception as exc:
            raise Exception("Error Accessing ELog API - Not able to get Jobs By")

    def get_jobs(self, token, base_url, site_id, job_id=None, page=1):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            if job_id:
                final_url = f"{base_url}/sites/{site_id}/jobs/{job_id}"
            else:
                final_url = f"{base_url}/sites/{site_id}/jobs?page={page}"
            response = requests.request("GET", final_url, headers=headers)
            return json.loads(response.text)
        except Exception as exc:
            raise Exception("Error Accessing ELog API - Not able to get Jobs")

    def acknowledge_job(self, token, base_url, site_id, job_id, job_data):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = (
                f"{base_url}/sites/{site_id}/jobs/{job_id}/workflow/assignment/accept"
            )
            payload = job_data
            response = requests.request(
                "POST", final_url, headers=headers, json=payload
            )
            if response.status_code < 300:
                return {"status": response.text}
            raise Exception(f"\n url: {final_url} \n response: {response.text}")
        except Exception as exc:
            raise Exception(
                f"Error Accessing ELog API - Not able to complete Job\n Explanation:{exc}"
            )

    def commence_job(self, token, base_url, site_id, job_id, job_data):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = (
                f"{base_url}/sites/{site_id}/jobs/{job_id}/workflow/operation/commence"
            )

            response = requests.request(
                "POST", final_url, headers=headers, data=job_data
            )
            if response.status_code < 300:
                return {"status": response.text}
            raise Exception(f"\n url: {final_url} \n response: {response.text}")
        except Exception as exc:
            raise Exception(
                f"Error Accessing ELog API - Not able to complete Job\n Explanation:{exc}"
            )

    def complete_job(self, token, base_url, site_id, job_id, job_data):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            final_url = (
                f"{base_url}/sites/{site_id}/jobs/{job_id}/workflow/operation/complete"
            )
            payload = job_data
            response = requests.request(
                "POST", final_url, headers=headers, data=payload
            )

            if response.status_code < 300:
                return {"status": response.text}
            raise Exception(f"\n url: {final_url} \n response: {response.text}")
        except Exception as exc:
            raise Exception(
                f"Error Accessing ELog API - Not able to complete Job\n Explanation:{exc}"
            )

    def complete_paperwork(self, token, base_url, site_id, job_id, job_data):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = f"{base_url}/sites/{site_id}/jobs/{job_id}/workflow/operation/complete-paperwork"
            payload = job_data
            response = requests.request(
                "POST", final_url, headers=headers, data=payload
            )

            if response.status_code < 300:
                return {"status": response.text}
            raise Exception(f"\n url: {final_url} \n response: {response.text}")
        except Exception as exc:
            raise Exception(
                f"Error Accessing ELog API - Not able to complete paperwork\n Explanation:{exc}"
            )

    def create_job(self, token, base_url, site_id, job_data):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = f"{base_url}/sites/{site_id}/jobs/reactive"
            payload = job_data
            response = requests.request(
                "POST", final_url, headers=headers, json=payload
            )
            if response.status_code < 300:
                return {
                    "status": response.status_code,
                    "data": json.loads(response.text),
                }

            raise Exception(f"\n url: {final_url} \n response: {response.text}")
        except Exception as exc:
            raise Exception(
                f"Error Accessing ELog API - Not able to create Job\n Explanation:{exc}"
            )

    def approve_job(self, token, base_url, site_id, job_id, status, job_data):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = (
                f"{base_url}/sites/{site_id}/jobs/{job_id}/workflow/approval/{status}"
            )
            payload = job_data
            response = requests.request(
                "POST", final_url, headers=headers, json=payload
            )
            if response.status_code < 300:
                return {"status": response.text}
            raise Exception(f"\n url: {final_url} \n response: {response.text}")
        except Exception as exc:
            raise Exception(
                f"Error Accessing ELog API - Not able to {status} Job\n Explanation:{exc}"
            )

    def request_job_extension(self, token, base_url, site_id, job_id, note):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = (
                f"{base_url}/sites/{site_id}/jobs/{job_id}/workflow/operation/extension"
            )
            payload = {"note": note}
            response = requests.request(
                "POST", final_url, headers=headers, json=payload
            )
            if response.status_code < 300:
                return {"status": response.text}
            raise Exception(f"\n url: {final_url} \n response: {response.text}")
        except Exception as exc:
            raise Exception(
                f"Error Accessing ELog API - Not able to complete Job\n Explanation:{exc}"
            )

    def accept_job_extension(self, token, base_url, site_id, job_id, status, job_data):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = f"{base_url}/sites/{site_id}/jobs/{job_id}/workflow/operation/extension/{status}"
            payload = job_data
            response = requests.request(
                "POST", final_url, headers=headers, json=payload
            )
            if response.status_code < 300:
                return {"status": response.text}
            raise Exception(f"\n url: {final_url} \n response: {response.text}")
        except Exception as exc:
            raise Exception(
                f"Error Accessing ELog API - Not able to complete Job\n Explanation:{exc}"
            )

    def get_file_data(self, token, base_url, file_data):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            }
            final_url = f"{base_url}/files"
            payload = json.dumps(file_data)
            response = requests.request(
                "POST", final_url, headers=headers, data=payload
            )
            if response.status_code < 300:
                return json.loads(response.text)
            raise Exception(f"\n url: {final_url} \n response: {response.text}")
        except Exception as exc:
            raise Exception(
                f"Error Accessing ELog API - Not able to get file data\n Explanation:{exc}"
            )

    def upload_file(self, token, google_bucket_data, file_name, file_type, file_content):
        try:
            url = f"https://storage.googleapis.com/{google_bucket_data.bucket}"

            payload = {
                "signature": google_bucket_data.signature,
                "Content-Disposition": google_bucket_data.content_disposition,
                "policy": google_bucket_data.policy,
                "success_action_redirect": google_bucket_data.success_action_redirect,
                "key": google_bucket_data.key,
                "GoogleAccessId": google_bucket_data.google_access_id,
                "bucket": google_bucket_data.bucket,
            }

            # Properly format the files parameter
            files = {
                "file": (file_name, file_content, file_type)
            }

            headers = {
                "Authorization": "Bearer " + token,
            }

            response = requests.post(
                url,
                headers=headers,
                data=payload,
                files=files
            )

            print(response.text)

        except:
            print(traceback.format_exc())
        return {"status": "OK"}
