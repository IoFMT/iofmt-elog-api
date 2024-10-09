# -*- coding: utf-8 -*-

import json
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

    def get_urls(self, token, base_url):
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
