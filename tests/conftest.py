import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Ensure we can import the script from the parent directory
# This mimics the setup in the original test file to ensure imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spotify_playlist_builder import SpotifyPlaylistBuilder


@pytest.fixture
def mock_spotify():
    """Mock the spotipy.Spotify client."""
    with patch("spotify_playlist_builder.spotipy.Spotify") as mock_cls:
        instance = MagicMock()
        mock_cls.return_value = instance
        # Mock successful authentication
        instance.current_user.return_value = {"id": "test_user_id"}
        yield instance


@pytest.fixture
def builder(mock_spotify):
    """Create a SpotifyPlaylistBuilder instance with mocked dependencies."""
    with patch("spotify_playlist_builder.SpotifyOAuth"):
        return SpotifyPlaylistBuilder("fake_client_id", "fake_client_secret")
