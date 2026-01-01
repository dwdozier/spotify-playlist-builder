import pytest
import httpx
from backend.app.main import app
from backend.app.models.user import User
from backend.app.core.auth.fastapi_users import current_active_superuser


@pytest.mark.asyncio
async def test_admin_stats_endpoint(db_session):
    """Test the admin stats endpoint."""
    # Mock a superuser
    mock_admin = User(
        id="admin_id",
        email="admin@example.com",
        is_superuser=True,
        is_active=True,
        is_verified=True,
    )

    from backend.app.db.session import get_async_session

    app.dependency_overrides[get_async_session] = lambda: db_session
    app.dependency_overrides[current_active_superuser] = lambda: mock_admin

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/admin/stats")
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "playlists" in data
        assert "connections" in data

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_admin_stats_unauthorized():
    """Test that non-admins cannot access stats."""
    # We don't override current_active_superuser here,
    # so it should return 401/403 based on how fastapi-users handles missing auth in tests
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/admin/stats")
        assert response.status_code in [401, 403]
