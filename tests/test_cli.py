from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from spotify_playlist_builder import app

runner = CliRunner()


def test_cli_build_success():
    """Test the build command."""
    with patch("spotify_playlist_builder.get_builder") as mock_get_builder:
        mock_builder = MagicMock()
        mock_get_builder.return_value = mock_builder
        # Create a dummy file for the argument
        with runner.isolated_filesystem():
            with open("playlist.json", "w") as f:
                f.write("{}")
            result = runner.invoke(app, ["build", "playlist.json", "--source", "env"])
            assert result.exit_code == 0
            mock_builder.build_playlist_from_json.assert_called_once()


def test_cli_build_error():
    """Test the build command handling errors."""
    with patch("spotify_playlist_builder.get_builder") as mock_get_builder:
        mock_builder = MagicMock()
        mock_builder.build_playlist_from_json.side_effect = Exception("Build failed")
        mock_get_builder.return_value = mock_builder
        with runner.isolated_filesystem():
            with open("playlist.json", "w") as f:
                f.write("{}")
            result = runner.invoke(app, ["build", "playlist.json"])
            assert result.exit_code == 1
            mock_builder.build_playlist_from_json.assert_called_once()


def test_cli_export_success():
    """Test the export command."""
    with patch("spotify_playlist_builder.get_builder") as mock_get_builder:
        mock_builder = MagicMock()
        mock_get_builder.return_value = mock_builder
        result = runner.invoke(app, ["export", "My Playlist", "out.json"])
        assert result.exit_code == 0
        mock_builder.export_playlist_to_json.assert_called_with("My Playlist", "out.json")


def test_cli_export_error():
    """Test export command error handling."""
    with patch("spotify_playlist_builder.get_builder") as mock_get_builder:
        mock_builder = MagicMock()
        mock_builder.export_playlist_to_json.side_effect = Exception("Export failed")
        mock_get_builder.return_value = mock_builder
        result = runner.invoke(app, ["export", "Playlist", "out.json"])
        assert result.exit_code == 1


def test_cli_backup_success():
    """Test the backup command."""
    with patch("spotify_playlist_builder.get_builder") as mock_get_builder:
        mock_builder = MagicMock()
        mock_get_builder.return_value = mock_builder
        result = runner.invoke(app, ["backup", "backups_dir"])
        assert result.exit_code == 0
        mock_builder.backup_all_playlists.assert_called_with("backups_dir")


def test_cli_backup_error():
    """Test backup command error handling."""
    with patch("spotify_playlist_builder.get_builder") as mock_get_builder:
        mock_builder = MagicMock()
        mock_builder.backup_all_playlists.side_effect = Exception("Backup failed")
        mock_get_builder.return_value = mock_builder
        result = runner.invoke(app, ["backup", "backups"])
        assert result.exit_code == 1


def test_cli_store_credentials():
    """Test storing credentials interactively."""
    with patch("spotify_playlist_builder.store_credentials_in_keyring") as mock_store:
        # Simulate user input: client_id, then client_secret
        result = runner.invoke(app, ["store-credentials"], input="my_id\nmy_secret\n")
        assert result.exit_code == 0
        mock_store.assert_called_with("my_id", "my_secret")


def test_cli_store_credentials_missing_input():
    """Test error when input is missing."""
    result = runner.invoke(app, ["store-credentials"], input="\n\n")  # Empty inputs
    assert result.exit_code == 1


def test_cli_store_credentials_exception():
    """Test exception handling in store-credentials command."""
    with patch(
        "spotify_playlist_builder.store_credentials_in_keyring",
        side_effect=Exception("Keyring error"),
    ):
        result = runner.invoke(app, ["store-credentials"], input="user\npass\n")
        assert result.exit_code == 1


def test_cli_main_verbose():
    """Test global options like verbose."""
    # Just checking it doesn't crash and sets level
    with patch("logging.basicConfig"):
        result = runner.invoke(app, ["--verbose", "build", "--help"])
        assert result.exit_code == 0


def test_cli_install_completion_success():
    """Test successful installation of zsh completion."""
    with (
        patch("pathlib.Path.home") as mock_home,
        patch("subprocess.run") as mock_run,
        patch("builtins.open", new_callable=MagicMock) as mock_open,
    ):
        # Setup mocks
        mock_omz = MagicMock()
        mock_omz.exists.return_value = True
        # Path configuration: home / .oh-my-zsh
        mock_home.return_value.__truediv__.return_value = mock_omz
        # Mock completions dir: omz / completions
        mock_completions = MagicMock()
        mock_omz.__truediv__.return_value = mock_completions
        # Mock target file: completions / _script
        mock_target = MagicMock()
        mock_completions.__truediv__.return_value = mock_target

        # Mock subprocess result
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "completion script content"

        result = runner.invoke(app, ["install-zsh-completion"])

        assert result.exit_code == 0
        # Check if subprocess was called to generate script
        mock_run.assert_called_once()
        # Check if file was written
        mock_open.assert_called_with(mock_target, "w")
        mock_open.return_value.__enter__.return_value.write.assert_called_with(
            "completion script content"
        )


def test_cli_install_completion_no_omz():
    """Test installation fails if Oh My Zsh is not found."""
    with patch("pathlib.Path.home") as mock_home:
        mock_omz = MagicMock()
        mock_omz.exists.return_value = False
        mock_home.return_value.__truediv__.return_value = mock_omz
        result = runner.invoke(app, ["install-zsh-completion"])
        assert result.exit_code == 1


def test_cli_install_completion_subprocess_error():
    """Test installation fails if completion generation fails."""
    with patch("pathlib.Path.home") as mock_home, patch("subprocess.run") as mock_run:
        mock_omz = MagicMock()
        mock_omz.exists.return_value = True
        mock_home.return_value.__truediv__.return_value = mock_omz
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Error generating"
        result = runner.invoke(app, ["install-zsh-completion"])
        assert result.exit_code == 1


def test_cli_install_completion_empty_script():
    """Test error when generated completion script is empty."""
    with (
        patch("pathlib.Path.home") as mock_home,
        patch("subprocess.run") as mock_run,
    ):
        mock_omz = MagicMock()
        mock_omz.exists.return_value = True
        mock_home.return_value.__truediv__.return_value = mock_omz
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""  # Empty output
        result = runner.invoke(app, ["install-zsh-completion"])
        assert result.exit_code == 1


def test_cli_uninstall_completion():
    """Test uninstall instruction command."""
    result = runner.invoke(app, ["uninstall-completion"])
    assert result.exit_code == 0
