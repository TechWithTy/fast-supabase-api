"""
Celery configuration for FastAPI project.

This file configures Celery for use with FastAPI. It does not rely on Django.
"""
import os
from celery import Celery
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file (optional)
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# You can use a Pydantic settings class if desired
broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "fastapi_project",
    broker=broker_url,
    backend=backend_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to verify Celery is working correctly."""
    print(f"Request: {self.request!r}")
