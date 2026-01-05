from taskiq_redis import ListQueueBroker
from backend.app.core.config import settings

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
