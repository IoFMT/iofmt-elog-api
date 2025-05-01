# -*- coding: utf-8 -*-

import json

from sqlalchemy import text

from entities.base import Config
from libs import config


class ConfigService:
    db = None

    def __init__(self, db):
        self.db = db

    def add_config(self, data: Config):
        # Insert the config
        stmt = text(config.CACHE_SQL_INSERT_CONFIG)
        stmt = stmt.bindparams(
            p1=data.api_key, p2=data.account_number, p3=data.user_name,
            p4=data.url, p5=data.created_at, p6=data.created_by
        )
        self.db.execute(stmt)
        self.db.commit()

        # Get the inserted user_id
        stmt = text("SELECT user_id FROM elogapi.config WHERE api_key = :p1")
        stmt = stmt.bindparams(p1=data.api_key)
        result = self.db.execute(stmt).fetchone()
        return result[0] if result else None

    def delete_config(self, user_id):
        stmt = text(config.CACHE_SQL_DELETE_CONFIG)
        stmt = stmt.bindparams(p1=user_id)
        self.db.execute(stmt)
        self.db.commit()

    def list_config(self):
        stmt = text("SELECT api_key, account_number, user_id, user_name, url, token, expiration, "
                    "created_at, created_by "
                    "FROM elogapi.config")
        result = self.db.execute(stmt).fetchall()

        results = []
        for res in result:
            results.append(
                {
                    "api_key": res[0],
                    "account_number": res[1],
                    "user_id": res[2],
                    "user_name": res[3],
                    "url": res[4],
                    "token": res[5],
                    "expiration": res[6],
                    "created_at": res[7],
                    "created_by": res[8],
                }
            )

        return results

    def select_config_by_user_id(self, user_id: int):
        stmt = text("SELECT user_id, api_key, user_name, account_number, url FROM elogapi.config where user_id = :p1")
        stmt = stmt.bindparams(p1=user_id)
        res = self.db.execute(stmt).fetchone()

        results = {
            "user_id": res[0],
            "api_key": res[1],
            "user_name": res[2],
            "account_number": res[3],
            "url": res[4],
        }

        return results

    def select_config_by_user_name_api_key(self, user_name: int, api_key: str):
        stmt = text("SELECT user_id, api_key, user_name, account_number, url FROM elogapi.config where user_name = :p1 and api_key = :p2")
        stmt = stmt.bindparams(p1=user_name, p2=api_key)
        res = self.db.execute(stmt).fetchone()

        results = {
            "user_id": res[0],
            "api_key": res[1],
            "user_name": res[2],
            "account_number": res[3],
            "url": res[4],
        }

        return results

    def select_config(self, api_key: str):
        stmt = text("SELECT user_id, api_key, user_name, account_number, url FROM elogapi.config where api_key = :p1")
        stmt = stmt.bindparams(p1=api_key)
        res = self.db.execute(stmt).fetchall()[0]

        results = {
            "user_id": res[0],
            "api_key": res[1],
            "user_name": res[2],
            "account_number": res[3],
            "url": res[4],
        }

        return results

    def exist_config(self, api_key: str):
        stmt = text("SELECT count(1) FROM elogapi.config where api_key = :p1")
        stmt = stmt.bindparams(p1=api_key)
        result = self.db.execute(stmt).fetchone()
        return True if result[0] > 0 else False

    def exist_config_by_user_id(self, user_id: int):
        stmt = text("SELECT count(1) FROM elogapi.config where user_id = :p1")
        stmt = stmt.bindparams(p1=user_id)
        result = self.db.execute(stmt).fetchone()
        return True if result[0] > 0 else False

    def select_token_by_user_id(self, user_id):
        stmt = text(
            "SELECT url, token, expiration, other_urls FROM elogapi.config where user_id = :p1"
        )
        stmt = stmt.bindparams(p1=user_id)
        result = self.db.execute(stmt).fetchone()

        if not result:
            return None

        # Handle NULL other_urls by defaulting to empty list/dict
        other_urls = result[3]
        parsed_other_urls = json.loads(other_urls) if other_urls is not None else []

        response = {
            "url": result[0],
            "token": result[1],
            "expiration": result[2],
            "other_urls": parsed_other_urls,
        }

        # Check if token is null and raise an exception if it is
        if response["token"] is None:
            raise Exception("Token is null or not available")

        return response

    def select_token(self, api_key):
        stmt = text(
            "SELECT url, token, expiration, other_urls FROM elogapi.config where api_key = :p1"
        )
        stmt = stmt.bindparams(p1=api_key)
        result = self.db.execute(stmt).fetchone()

        if not result:
            return None

        # Handle NULL other_urls by defaulting to empty list/dict
        other_urls = result[3]
        parsed_other_urls = json.loads(other_urls) if other_urls is not None else []

        response = {
            "url": result[0],
            "token": result[1],
            "expiration": result[2],
            "other_urls": parsed_other_urls,
        }

        # Check if token is null and raise an exception if it is
        if response["token"] is None:
            raise Exception("Token is null or not available")

        return response

    def update_token(self, api_key, token, expiration, other_urls):
        stmt = text(
            "UPDATE elogapi.config SET token = :p2 , expiration = :p3, other_urls = :p4 where api_key = :p1"
        )
        stmt = stmt.bindparams(p1=api_key, p2=token, p3=expiration, p4=other_urls)
        self.db.execute(stmt)
        self.db.commit()
