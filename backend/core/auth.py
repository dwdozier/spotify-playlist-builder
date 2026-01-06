import logging
from typing import Tuple
from backend.app.core.config import settings

logger = logging.getLogger("backend.core.auth")


def get_credentials_from_env(silent: bool = False) -> Tuple[str, str] | None:
    """Get credentials from .env file or environment variables."""

    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET

    if not client_id or not client_secret:
        if silent:
            return None
        raise Exception(
            "Error: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET not found in environment.\n"
            "Create a .env file with:\n"
            "  SPOTIFY_CLIENT_ID=your_id\n"
            "  SPOTIFY_CLIENT_SECRET=your_secret"
        )
    return client_id, client_secret


def get_credentials() -> Tuple[str, str]:
    """Get Spotify credentials from environment."""
    result = get_credentials_from_env()
    if result is None:
        raise Exception("Failed to load credentials from environment.")
    return result


def get_builder():
    """Helper to initialize SpotifyPlaylistBuilder with credentials."""
    from .client import SpotifyPlaylistBuilder

    logger.info("Fetching credentials from environment...")

    client_id, secret = get_credentials()
    return SpotifyPlaylistBuilder(client_id, secret)
