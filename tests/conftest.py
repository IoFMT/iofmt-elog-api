import os
import random
import string

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def admin_api_key():
    return os.environ.get("ADMIN_PWD")


@pytest.fixture(scope="session", autouse=True)
def random_username():
    length = 8
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
