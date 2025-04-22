import pytest

pytestmark = pytest.mark.anyio("asyncio")

async def test_async_only():
    assert True
