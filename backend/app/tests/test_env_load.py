import os

from app.tests.utils.env_loader import load_env


def test_env_vars_loaded():
    load_env()
    print("PROJECT_NAME:", os.environ.get("PROJECT_NAME"))
    print("FIRST_SUPERUSER:", os.environ.get("FIRST_SUPERUSER"))
    print("FIRST_SUPERUSER_PASSWORD:", os.environ.get("FIRST_SUPERUSER_PASSWORD"))

if __name__ == "__main__":
    test_env_vars_loaded()
