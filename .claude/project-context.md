# Spotify Playlist Builder - Project Context

## Overview

A Python CLI tool that creates Spotify playlists programmatically from JSON data files. The tool searches for tracks, creates playlists, and handles batch operations with the Spotify API.

## Architecture

### Core Components

**`spotify_playlist_builder.py`** - Main application module containing:
- `SpotifyPlaylistBuilder` class: Core playlist operations
- Credential management functions: Support for .env and 1Password
- CLI entry point: Argument parsing and execution flow

**`main.py`** - Minimal entry point (currently just a placeholder)

**`playlists/`** - Directory containing JSON playlist definitions

### Key Design Decisions

1. **OAuth Authentication**: Uses SpotifyOAuth for user authentication (required for playlist creation/modification)
2. **Multiple Credential Sources**: Users can choose between:
   - `.env` files (simplest, good for development)
   - macOS Keychain via `keyring` (recommended - secure and convenient)
   - 1Password (for teams already using 1Password)
3. **Smart Playlist Updates**: Automatically detects existing playlists and updates them instead of creating duplicates
4. **Studio Album Preference**: Searches prioritize studio albums over compilations/greatest hits/live versions
5. **Optional Album Specification**: JSON tracks can specify an album name to ensure the correct version is used
6. **Batch Operations**: Tracks are added in batches of 100 to respect Spotify API limits
7. **Graceful Failure**: Tracks that can't be found are reported but don't stop the entire process
8. **Public Playlists**: All created playlists are public by default

## Data Flow

```
JSON File → Parse tracks → Search Spotify (prefer studio albums) → Check if playlist exists
  ↓
  ├─ Exists & different → Clear & rebuild with new tracks
  ├─ Exists & same → Skip (no changes needed)
  └─ Doesn't exist → Create new → Batch add tracks → Report results
```

## Dependencies

- **spotipy**: Official Spotify API wrapper
- **python-dotenv**: Environment variable management (.env file support)
- **keyring**: Secure credential storage via OS keychain
- **uv**: Package and environment management

## Common Workflows

### Adding a New Playlist
1. Create JSON file in `playlists/` directory
2. Structure: `{"name": "...", "description": "...", "tracks": [{"artist": "...", "track": "...", "album": "..."}]}`
   - `album` field is optional but recommended for tracks that appear on multiple albums
3. Run: `uv run python spotify_playlist_builder.py playlists/your-file.json`
4. First run will open browser for OAuth authorization

### Updating an Existing Playlist
1. Modify the JSON file (add/remove/reorder tracks, or specify preferred albums)
2. Run the same command - it will detect the existing playlist and update it
3. Script will replace compilation versions with studio versions when applicable

### Testing Credential Sources
- **.env** (default): `uv run python spotify_playlist_builder.py <json>`
- **macOS Keychain**: `uv run python spotify_playlist_builder.py <json> --source keyring`
- **1Password**: `uv run python spotify_playlist_builder.py <json> --source 1password --vault VaultName`

### Managing Credentials

**Store in macOS Keychain (recommended):**
```bash
uv run python spotify_playlist_builder.py --store-credentials
```

**List 1Password Vaults:**
```bash
uv run python spotify_playlist_builder.py --list-vaults
```

**1Password Vault Names by Account Type:**
- Individual: Usually "Personal" or "Private"
- Family: Usually "Private" or "Shared"
- Team/Business: Usually "Employee", "Private", or custom team vault names

### Development Setup
```bash
uv sync                          # Install dependencies
source .venv/bin/activate        # Activate environment
```

## API Limits & Constraints

- Spotify API batch limit: 100 tracks per request
- Search results: Queries up to 10 results to find studio album versions
- OAuth required: Must authenticate via browser on first run
- Redirect URI: Must configure `https://127.0.0.1:8888/callback` in Spotify Developer Dashboard
- Requires valid Spotify Developer credentials (Client ID + Secret)

## Code Conventions

### Language & Tools
- **Python Version**: 3.11+ required
- **Package Manager**: uv (not pip)
- **Virtual Environment**: .venv
- **Formatter**: black with 100 character line length
- **Linter**: ruff
- **Docstring Style**: Google format

### Project Structure
- **Main Module**: `spotify_playlist_builder.py`
- **Test Pattern**: `test_*.py` (when added)
- **Config Files**: `pyproject.toml`, `.env`, `.python-version`
- **Playlists Directory**: `playlists/`

### Coding Practices
- Line length: 100 characters (enforced by black/ruff)
- Type hints: Not currently used but could be added
- Error handling: Exception-based with user-friendly messages
- Credentials: Must be in .env or 1Password, never hardcoded
- Always use `uv run` for executing scripts to ensure correct environment

## Future Enhancements

Potential areas for improvement:
- ✅ ~~Playlist update/modification capabilities~~ (Implemented)
- ✅ ~~Better track matching with studio album preference~~ (Implemented)
- Add support for private playlists (currently all public)
- Support for playlist deduplication (remove duplicate tracks)
- Add tests (pytest structure already in pyproject.toml)
- Type annotations throughout
- Verbose mode to show which album each track was found on
- Cache search results to speed up re-runs
- Batch playlist creation from multiple JSON files
- Export existing Spotify playlists to JSON format

## Security Notes

- **Never commit .env files** - Always in .gitignore
- **1Password recommended** for team environments
- Credentials are read-only (no write operations to credential stores)
- All Spotify operations use official API with proper authentication

## Troubleshooting

**Track Not Found**: Check artist/track spelling in JSON - Spotify search is forgiving but exact names work best. Consider adding `"album"` field for tracks with multiple versions.

**Wrong Album Version**: Add the `"album"` field to your track in the JSON to specify which album to prefer.

**OAuth/Authentication Issues**:
- Ensure redirect URI `https://127.0.0.1:8888/callback` is configured in Spotify Developer Dashboard
- Delete `.cache` file and re-authenticate if having issues
- Verify SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env

**1Password CLI Issues**:
- Run `python spotify_playlist_builder.py --list-vaults` to see your available vaults
- Ensure you're authenticated: `eval $(op signin)`
- Specify the correct vault with `--vault VaultName`
- Vault names vary by account type (Personal/Private/Employee)
- Item must be named 'SpotifyPlaylistBuilder' in the specified vault
- Fields must be named 'client_id' and 'client_secret'

**Import Errors**: Ensure dependencies are installed (`uv sync`) and use `uv run` to execute scripts

**Playlist Not Updating**: Script detects changes by comparing track URIs. If tracks appear the same but you want to force an update, temporarily change the playlist name.
