from unittest.mock import MagicMock, patch
from backend.app.core.tasks import create_playlist_task


async def test_create_playlist_task():
    """Test the create_playlist_task background worker."""
    from unittest.mock import AsyncMock

    with patch("backend.core.providers.spotify.SpotifyProvider") as mock_provider_cls:
        mock_provider = MagicMock()
        mock_provider.create_playlist = AsyncMock(return_value="pl_id")
        mock_provider.add_tracks_to_playlist = AsyncMock()
        mock_provider_cls.return_value = mock_provider

        pl_id = await create_playlist_task("My Task Playlist", ["uri:1"], "token")

        assert pl_id == "pl_id"
        mock_provider.create_playlist.assert_called_once_with("My Task Playlist")
        mock_provider.add_tracks_to_playlist.assert_called_once_with("pl_id", ["uri:1"])


async def test_purge_deleted_playlists_task():
    """Test the purge_deleted_playlists_task."""
    from backend.app.core.tasks import purge_deleted_playlists_task
    from unittest.mock import AsyncMock

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    mock_result = MagicMock()
    mock_result.rowcount = 5
    mock_session.execute.return_value = mock_result

    # Mock async context manager
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    with patch("backend.app.core.tasks.async_session_maker") as mock_maker:
        mock_maker.return_value = mock_session

        result = await purge_deleted_playlists_task()

        assert result == "Purged 5 playlists"
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
