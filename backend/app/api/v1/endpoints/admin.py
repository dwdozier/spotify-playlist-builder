from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.db.session import get_async_session
from backend.app.core.auth.fastapi_users import current_active_superuser
from backend.app.models.user import User
from backend.app.models.playlist import Playlist
from backend.app.models.service_connection import ServiceConnection
from backend.app.models.user import OAuthAccount

router = APIRouter()


@router.get("/stats")
async def get_system_stats(
    user: User = Depends(current_active_superuser),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Get high-level system statistics for the admin dashboard.
    """
    user_count = await db.execute(select(func.count(User.id)))
    playlist_count = await db.execute(select(func.count(Playlist.id)))
    connection_count = await db.execute(select(func.count(ServiceConnection.id)))
    oauth_count = await db.execute(select(func.count(OAuthAccount.id)))

    return {
        "users": user_count.scalar(),
        "playlists": playlist_count.scalar(),
        "connections": connection_count.scalar(),
        "oauth_accounts": oauth_count.scalar(),
    }
