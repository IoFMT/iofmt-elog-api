# -*- coding: utf-8 -*-

import json

from sqlalchemy import text


from libs import config
from entities.base import Config


class ConfigService:
    db = None

    def __init__(self, db):
        self.db = db

    def add_config(self, data: Config):
        stmt = text(config.CACHE_SQL_INSERT_CONFIG)
        stmt = stmt.bindparams(p1=data.api_key, p2=data.user_name, p3=data.user_pwd)
        self.db.execute(stmt)
        self.db.commit()

    def delete_config(self, api_key):
        stmt = text(config.CACHE_SQL_DELETE_CONFIG)
        stmt = stmt.bindparams(p1=api_key)
        self.db.execute(stmt)
        self.db.commit()

    def list_config(self):
        stmt = text("SELECT * FROM elogapi.config")
        result = self.db.execute(stmt).fetchall()

        results = []
        for res in result:
            results.append(
                {
                    "api_key": res[0],
                    "user_name": res[1],
                    "user_pwd": res[2],
                    "token": res[3],
                }
            )

        return results

    def select_config(self, api_key):
        stmt = text("SELECT * FROM elogapi.config where api_key = :p1")
        stmt = stmt.bindparams(p1=api_key)
        res = self.db.execute(stmt).fetchone()

        results = {
            "api_key": res[0],
            "user_name": res[1],
            "user_pwd": res[2],
            "token": res[3],
        }

        return results

    def exist_config(self, api_key):
        stmt = text("SELECT count(1) FROM elogapi.config where api_key = :p1")
        stmt = stmt.bindparams(p1=api_key)
        result = self.db.execute(stmt).fetchone()
        return True if result[0] > 0 else False

    def select_token(self, api_key):
        stmt = text("SELECT token FROM elogapi.config where api_key = :p1")
        stmt = stmt.bindparams(p1=api_key)
        result = self.db.execute(stmt).fetchone()

        return result[0] if result else None

    def update_token(self, api_key, token):
        stmt = text("UPDATE elogapi.config SET token = :p2 where api_key = :p1")
        stmt = stmt.bindparams(p1=api_key, p2=token)
        result = self.db.execute(stmt).fetchone()

        return result[0] if result else None
