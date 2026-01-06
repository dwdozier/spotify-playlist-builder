from datetime import datetime, timedelta, timezone
from sqlalchemy import delete
from taskiq_redis import ListQueueBroker
from backend.app.core.config import settings
from backend.app.db.session import async_session_maker
from backend.app.models.playlist import Playlist

broker = ListQueueBroker(str(settings.REDIS_URL))


@broker.task
async def create_playlist_task(
    playlist_name: str,
    track_uris: list[str],
    auth_token: str,
) -> str:
    """Background task to create a playlist on Spotify."""
    from backend.core.providers.spotify import SpotifyProvider

    provider = SpotifyProvider(auth_token=auth_token)
    playlist_id = await provider.create_playlist(playlist_name)
    await provider.add_tracks_to_playlist(playlist_id, track_uris)

    return playlist_id


@broker.task
async def purge_deleted_playlists_task() -> str:
    """
    Purge playlists soft-deleted more than 30 days ago.
    """
    async with async_session_maker() as session:
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)

        stmt = delete(Playlist).where(Playlist.deleted_at <= cutoff)
        result = await session.execute(stmt)
        await session.commit()
        return f"Purged {result.rowcount} playlists"  # type: ignore
