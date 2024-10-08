# -*- coding: utf-8 -*-
"""This module contains the database configuration."""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from libs.config import CACHE_DB

engine = None
SessionLocal = None

if CACHE_DB:
    engine = create_engine(CACHE_DB, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_metadata():
    """
    This is needed to autogenerate revisions to work in alembic
    """
    from entities.base import Config

    return Base.metadata


def upgrade_db():
    """Invokes alembic to bring the database to the latest version"""
    pass


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
