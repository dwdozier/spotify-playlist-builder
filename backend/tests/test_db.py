import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.user import User
from backend.app.models.playlist import Playlist
from backend.app.models.service_connection import ServiceConnection
from sqlalchemy import select


@pytest.mark.asyncio
async def test_user_model(db_session: AsyncSession):
    """Test creating a user."""
    user = User(
        email="test@example.com",
        hashed_password="hashed",
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )
    db_session.add(user)
    await db_session.commit()

    result = await db_session.execute(select(User).filter(User.email == "test@example.com"))  # type: ignore
    db_user = result.unique().scalar_one()
    assert db_user.email == "test@example.com"
    assert isinstance(db_user.id, uuid.UUID)


@pytest.mark.asyncio
async def test_playlist_model(db_session: AsyncSession):
    """Test creating a playlist linked to a user."""
    user = User(email="p@example.com", hashed_password="h")
    db_session.add(user)
    await db_session.flush()  # Get user id

    playlist = Playlist(user_id=user.id, name="Test Playlist", content_json={"tracks": []})
    db_session.add(playlist)
    await db_session.commit()

    result = await db_session.execute(select(Playlist).where(Playlist.name == "Test Playlist"))
    db_pl = result.scalar_one()
    assert db_pl.name == "Test Playlist"
    assert db_pl.user_id == user.id


@pytest.mark.asyncio
async def test_service_connection_model(db_session: AsyncSession):
    """Test creating a service connection with credentials."""
    user = User(email="s@example.com", hashed_password="h")
    db_session.add(user)
    await db_session.flush()

    # Test with full credentials
    conn = ServiceConnection(
        user_id=user.id,
        provider_name="spotify",
        provider_user_id="spotify_user_1",
        access_token="access",
        refresh_token="refresh",
        credentials={"client_id": "cid", "client_secret": "csec"},
    )
    db_session.add(conn)
    await db_session.commit()
    await db_session.refresh(conn)

    assert conn.is_connected is True
    assert conn.client_id == "cid"
    assert conn.has_secret is True
    # Verify encryption works by checking it's still a dict when read back
    assert conn.credentials == {"client_id": "cid", "client_secret": "csec"}

    # Test disconnected / pending state
    conn_pending = ServiceConnection(
        user_id=user.id,
        provider_name="spotify",
        provider_user_id="PENDING",
        access_token="",
        credentials={"client_id": "cid2"},
    )
    db_session.add(conn_pending)
    await db_session.commit()
    await db_session.refresh(conn_pending)

    assert conn_pending.is_connected is False
    assert conn_pending.client_id == "cid2"
    assert conn_pending.has_secret is False

    # Test with NO credentials (None)
    conn_none = ServiceConnection(
        user_id=user.id,
        provider_name="spotify",
        provider_user_id="PENDING_NONE",
        access_token="",
        credentials=None,
    )
    db_session.add(conn_none)
    await db_session.commit()
    await db_session.refresh(conn_none)

    assert conn_none.credentials is None
    assert conn_none.client_id is None
    assert conn_none.has_secret is False
