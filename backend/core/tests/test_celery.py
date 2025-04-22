import pytest
from celery import Celery

# Configure a test Celery app (adjust broker/backend as needed)
celery_app = Celery(
    'test_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def add(x: int, y: int) -> int:
    """Simple test task for Celery."""
    return x + y

@pytest.mark.anyio
async def test_celery_add_task():
    """
    Test that Celery can enqueue and execute a simple task.
    """
    result = add.apply_async((2, 3))
    output = result.get(timeout=10)
    assert output == 5
    # Clean up result
    result.forget()
