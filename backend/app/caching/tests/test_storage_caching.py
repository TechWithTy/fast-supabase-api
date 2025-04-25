import pytest
import hashlib
import time
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.caching.utils.redis_cache import redis_cache, get_cached_result, get_or_set_cache
from app.core.config import settings
from app.models import User
from sqlmodel import Session

# Fixtures for DB, user, token, and client
@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def db():
    from app.core.db import engine
    with Session(engine) as session:
        yield session

@pytest.fixture(scope="function")
def test_user(db):
    user = User(
        email="test@example.com",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
        hashed_password="$2b$12$KIXQJz4Q7Z0w0V6VqTgL7O6c9v1CwQxK1QOQ5ZyQ5ZyQ5ZyQ5ZyQ5"  # bcrypt for 'testpassword'
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()

@pytest.fixture(scope="function")
def user_token(client, test_user):
    response = client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data={"username": test_user.email, "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture(autouse=True)
def clear_redis_cache():
    redis_cache.flushdb()
    yield
    redis_cache.flushdb()

# Test data
TEST_BUCKET = "test-bucket"
TEST_PATH = "test/path"
TEST_FILE_DATA = "base64encodeddata"

# 1. Test that list_objects properly caches storage listings
def test_list_objects_caching(client, user_token):
    mock_response = [{"name": "file1.txt", "size": 1024}]
    headers = {"Authorization": f"Bearer {user_token}"}
    with patch("app.api.based_routes.db.storage.SupabaseStorageService.list_objects", return_value=mock_response) as mock_list_objects:
        # First call (cache miss)
        resp1 = client.get(f"/api/client/storage/list/?bucket_name={TEST_BUCKET}&path={TEST_PATH}", headers=headers)
        assert resp1.status_code == 200
        assert resp1.json() == mock_response
        mock_list_objects.assert_called_once_with(TEST_BUCKET, TEST_PATH)
        # Second call (should hit cache, so no new call)
        mock_list_objects.reset_mock()
        resp2 = client.get(f"/api/client/storage/list/?bucket_name={TEST_BUCKET}&path={TEST_PATH}", headers=headers)
        assert resp2.status_code == 200
        assert resp2.json() == mock_response
        mock_list_objects.assert_not_called()

# 2. Test that list_objects returns cached data on cache hit
def test_list_objects_cache_hit(client, user_token):
    mock_response = [{"name": "cached_file.txt", "size": 2048}]
    path_hash = hashlib.sha256(TEST_PATH.encode()).hexdigest()
    cache_key = f"storage:list:{TEST_BUCKET}:{path_hash}"
    redis_cache.set(cache_key, TEST_FILE_DATA.encode(), ex=300)
    headers = {"Authorization": f"Bearer {user_token}"}
    with patch("app.api.based_routes.db.storage.SupabaseStorageService.list_objects") as mock_list_objects:
        resp = client.get(f"/api/client/storage/list/?bucket_name={TEST_BUCKET}&path={TEST_PATH}", headers=headers)
        assert resp.status_code == 200
        # The endpoint should return the cached value, so storage is not called
        mock_list_objects.assert_not_called()

# 3. Test that upload_file invalidates relevant cache entries
def test_upload_file_invalidates_cache(client, user_token):
    path_hash1 = hashlib.md5(TEST_PATH.encode()).hexdigest()
    path_hash2 = hashlib.md5("other/path".encode()).hexdigest()
    cache_key1 = f"storage:list:{TEST_BUCKET}:{path_hash1}"
    cache_key2 = f"storage:list:{TEST_BUCKET}:{path_hash2}"
    cache_key3 = f"storage:list:other-bucket:{path_hash1}"
    redis_cache.set(cache_key1, b"test1", ex=300)
    redis_cache.set(cache_key2, b"test2", ex=300)
    redis_cache.set(cache_key3, b"test3", ex=300)
    headers = {"Authorization": f"Bearer {user_token}"}
    with patch("app.api.based_routes.db.storage.SupabaseStorageService.upload_file", return_value={"Key": TEST_PATH}) as mock_upload_file:
        resp = client.post(
            "/api/client/storage/upload/",
            json={"bucket_name": TEST_BUCKET, "path": TEST_PATH, "content": TEST_FILE_DATA},
            headers=headers,
        )
        assert resp.status_code == 201
        assert "uploaded successfully" in resp.json().get("message", "")
        mock_upload_file.assert_called_once_with(TEST_BUCKET, TEST_PATH, TEST_FILE_DATA)
        # Check cache invalidation (cache_key1 and cache_key2 should be gone, cache_key3 should remain)
        assert redis_cache.get(cache_key1) is None
        assert redis_cache.get(cache_key2) is None
        assert redis_cache.get(cache_key3) == b"test3"

# 4. Test that delete_file invalidates relevant cache entries
def test_delete_file_invalidates_cache(client, user_token):
    path_hash1 = hashlib.md5(TEST_PATH.encode()).hexdigest()
    path_hash2 = hashlib.md5("other/path".encode()).hexdigest()
    cache_key1 = f"storage:list:{TEST_BUCKET}:{path_hash1}"
    cache_key2 = f"storage:list:{TEST_BUCKET}:{path_hash2}"
    cache_key3 = f"storage:list:other-bucket:{path_hash1}"
    redis_cache.set(cache_key1, b"test1", ex=300)
    redis_cache.set(cache_key2, b"test2", ex=300)
    redis_cache.set(cache_key3, b"test3", ex=300)
    file_path = f"{TEST_PATH}/file.txt"
    headers = {"Authorization": f"Bearer {user_token}"}
    with patch("app.api.based_routes.db.storage.SupabaseStorageService.delete_file", return_value=None) as mock_delete_file:
        resp = client.delete(
            "/api/client/storage/delete/",
            json={"bucket_name": TEST_BUCKET, "path": file_path},
            headers=headers,
        )
        assert resp.status_code == 200
        assert "deleted successfully" in resp.json().get("message", "")
        mock_delete_file.assert_called_once_with(TEST_BUCKET, file_path)
        # Check cache invalidation (cache_key1 and cache_key2 should be gone, cache_key3 should remain)
        assert redis_cache.get(cache_key1) is None
        assert redis_cache.get(cache_key2) is None
        assert redis_cache.get(cache_key3) == b"test3"

# 5. Test performance improvement with caching
def test_list_objects_performance(client, user_token):
    mock_storage_response = [{"name": "file1.txt", "size": 1024}]
    headers = {"Authorization": f"Bearer {user_token}"}
    with patch("app.api.based_routes.db.storage.SupabaseStorageService.list_objects", return_value=mock_storage_response) as mock_list_objects:
        url = f"/api/client/storage/list/?bucket_name={TEST_BUCKET}&path={TEST_PATH}"
        # First request (cache miss)
        start_time = time.time()
        resp1 = client.get(url, headers=headers)
        first_request_time = time.time() - start_time
        assert resp1.status_code == 200
        # Second request (cache hit)
        start_time = time.time()
        resp2 = client.get(url, headers=headers)
        second_request_time = time.time() - start_time
        assert resp2.status_code == 200
        # The second request should be faster
        assert second_request_time < first_request_time
