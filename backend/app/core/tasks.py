import os
from taskiq_redis import ListQueueBroker

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
broker = ListQueueBroker(redis_url)


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
