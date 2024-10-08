# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

# Initialize the variables

GLOBAL_API_KEY = None
WEB_API_URL = None
SCOPE = None
CLIENT_ID = None
AUTHORITY = None
CACHEFILE = None
SFG20_URL = None
THROTTLE_RATE = 100
THROTTLE_RATE_EXT = 50
THROTTLE_TIME = 60

# Load the environment variables
load_dotenv()

# Set the variables from the environment
if "GLOBAL_API_KEY" in os.environ:
    GLOBAL_API_KEY = os.environ["GLOBAL_API_KEY"]

# -------------------------------------------------
# Cache DB configuration
# -------------------------------------------------
if "CACHE_DB_HOST" in os.environ:
    CACHE_DB_HOST = os.environ["CACHE_DB_HOST"]

if "CACHE_DB_USER" in os.environ:
    CACHE_DB_USER = os.environ["CACHE_DB_USER"]

if "CACHE_DB_PWD" in os.environ:
    CACHE_DB_PWD = os.environ["CACHE_DB_PWD"]

# CACHE_DB = "data/cache.db"
CACHE_DB = f"postgresql://{CACHE_DB_USER}:{CACHE_DB_PWD}@{CACHE_DB_HOST}/postgres"

CACHE_SQL_INSERT_CONFIG = """INSERT INTO elogapi.config (api_key, user_name, user_pwd) VALUES (:p1, :p2, :p3)"""

CACHE_SQL_DELETE_CONFIG = """DELETE FROM elogapi.config WHERE api_key = :p1"""

ADMIN_USER = None
ADMIN_PWD = None

if "ADMIN_USER" in os.environ:
    ADMIN_USER = os.environ.get("ADMIN_USER")

if "ADMIN_PWD" in os.environ:
    ADMIN_PWD = os.environ.get("ADMIN_PWD")


# -------------------------------------------------
# API Documentation
# -------------------------------------------------

tags_metadata = [
    {
        "name": "Basic",
        "description": "Endpoint without authentication to check the API status.",
    },
    {
        "name": "Configuration",
        "description": "Endpoints to access the configuration data.",
    },
]
