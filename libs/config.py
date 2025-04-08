# -*- coding: utf-8 -*-
import os

from diskcache import Cache
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

AZAD_TENANT_ID = None
AZAD_CLIENT_ID = None
AZAD_CLIENT_SECRET = None
AZAD_REDIRECT_URI = None
AZAD_AUTH_HOST = None
AZAD_SESSION_SECRET = None
HOME_URL = None

JWT_SECRET_KEY = None
MEMORY_CACHE_MAX_SIZE = None
MEMORY_CACHE_TTL_SECONDS = None

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

CACHE_SQL_INSERT_CONFIG = """INSERT INTO elogapi.config
                          (api_key, account_number, user_name, url, created_at, created_by)
                          VALUES (:p1, :p2, :p3, :p4, :p5, :p6)"""

CACHE_SQL_DELETE_CONFIG = """DELETE FROM elogapi.config WHERE api_key = :p1"""

ADMIN_USER = None
ADMIN_PWD = None

if "ADMIN_USER" in os.environ:
    ADMIN_USER = os.environ.get("ADMIN_USER")
if "ADMIN_PWD" in os.environ:
    ADMIN_PWD = os.environ.get("ADMIN_PWD")

if "AZURE_AD_TENANT_ID" in os.environ:
    AZAD_TENANT_ID = os.environ.get("AZURE_AD_TENANT_ID")
if "AZURE_AD_CLIENT_ID" in os.environ:
    AZAD_CLIENT_ID = os.environ.get("AZURE_AD_CLIENT_ID")
if "AZURE_AD_CLIENT_SECRET" in os.environ:
    AZAD_CLIENT_SECRET = os.environ.get("AZURE_AD_CLIENT_SECRET")
if "AZURE_AD_REDIRECT_URI" in os.environ:
    AZAD_REDIRECT_URI = os.environ.get("AZURE_AD_REDIRECT_URI")
if "AZURE_AD_AUTH_HOST" in os.environ:
    AZAD_AUTH_HOST = os.environ.get("AZURE_AD_AUTH_HOST")
if "SESSION_SECRET" in os.environ:
    AZAD_SESSION_SECRET = os.environ.get("SESSION_SECRET")
if "HOME_URL" in os.environ:
    HOME_URL = os.environ.get("HOME_URL")
if "JWT_SECRET_KEY" in os.environ:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if "MEMORY_CACHE_MAX_SIZE" in os.environ:
    MEMORY_CACHE_MAX_SIZE = int(os.environ.get("MEMORY_CACHE_MAX_SIZE"))
if "MEMORY_CACHE_TTL_SECONDS" in os.environ:
    MEMORY_CACHE_TTL_SECONDS = int(os.environ.get("MEMORY_CACHE_TTL_SECONDS"))

AZAD_AUTHORITY = f"{AZAD_AUTH_HOST}/{AZAD_TENANT_ID}"
AZAD_AUTHORIZE_ENDPOINT = f"{AZAD_AUTHORITY}/oauth2/v2.0/authorize"
AZAD_TOKEN_ENDPOINT = f"{AZAD_AUTHORITY}/oauth2/v2.0/token"

CACHE_DIR = "/app/cache"
os.makedirs(CACHE_DIR, exist_ok=True)
app_cache = Cache(directory=CACHE_DIR, timeout=MEMORY_CACHE_TTL_SECONDS)

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
    {
        "name": "Login",
        "description": "Endpoints to login to the Elog API.",
    },
    {
        "name": "ELogs",
        "description": "Endpoints to the Elog API.",
    },
]
