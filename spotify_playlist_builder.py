import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import sys
import os
import subprocess
from pathlib import Path

try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False


# Credential Management Functions
def get_credentials_from_env():
    """Get credentials from .env file."""
    from dotenv import load_dotenv

    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise Exception(
            "Error: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET not found in .env file.\n"
            "Create a .env file with:\n"
            "  SPOTIFY_CLIENT_ID=your_id\n"
            "  SPOTIFY_CLIENT_SECRET=your_secret"
        )

    return client_id, client_secret


def list_1password_vaults():
    """List available 1Password vaults."""
    try:
        result = subprocess.run("op vault list", shell=True, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print("Available 1Password vaults:")
            print(result.stdout)
        else:
            print("Error listing vaults. Make sure you're signed in: eval $(op signin)")
    except FileNotFoundError:
        print("1Password CLI not found. Install it at:")
        print("https://developer.1password.com/docs/cli/get-started")


def get_credentials_from_1password(vault="Private", item="SpotifyPlaylistBuilder", id_field="client_id", secret_field="client_secret"):
    """Get credentials from 1Password vault."""
    try:
        cmd_id = f'op read "op://{vault}/{item}/{id_field}"'
        cmd_secret = f'op read "op://{vault}/{item}/{secret_field}"'

        result_id = subprocess.run(cmd_id, shell=True, capture_output=True, text=True, check=False)
        result_secret = subprocess.run(cmd_secret, shell=True, capture_output=True, text=True, check=False)

        if result_id.returncode != 0 or result_secret.returncode != 0:
            error_msg = result_id.stderr or result_secret.stderr
            raise Exception(
                f"Failed to fetch from 1Password vault '{vault}'.\n"
                f"\nCommon vault names by account type:\n"
                f"  • Individual accounts: 'Personal' or 'Private'\n"
                f"  • Family accounts: 'Private' or 'Shared'\n"
                f"  • Team/Business accounts: 'Employee', 'Private', or custom team vaults\n"
                f"\nTo see your available vaults:\n"
                f"  python spotify_playlist_builder.py --list-vaults\n"
                f"\nThen specify the correct vault:\n"
                f"  python spotify_playlist_builder.py playlist.json --source 1password --vault YourVaultName\n"
                f"\nMake sure:\n"
                f"  1. You're authenticated: eval $(op signin)\n"
                f"  2. Item named '{item}' exists in vault '{vault}'\n"
                f"  3. Fields '{id_field}' and '{secret_field}' exist on that item\n"
                f"\nError details: {error_msg}"
            )

        client_id = result_id.stdout.strip()
        client_secret = result_secret.stdout.strip()

        return client_id, client_secret

    except FileNotFoundError:
        raise Exception(
            "1Password CLI not found. Install it at:\n"
            "https://developer.1password.com/docs/cli/get-started"
        )


def get_credentials_from_keyring(service="spotify-playlist-builder"):
    """Get credentials from macOS Keychain (or OS credential store)."""
    if not KEYRING_AVAILABLE:
        raise Exception(
            "keyring library not available. Install it with:\n"
            "  uv sync"
        )

    client_id = keyring.get_password(service, "client_id")
    client_secret = keyring.get_password(service, "client_secret")

    if not client_id or not client_secret:
        raise Exception(
            f"Credentials not found in keychain.\n"
            f"To store credentials, run:\n"
            f"  python -c \"import keyring; keyring.set_password('{service}', 'client_id', 'YOUR_CLIENT_ID')\"\n"
            f"  python -c \"import keyring; keyring.set_password('{service}', 'client_secret', 'YOUR_CLIENT_SECRET')\"\n"
            f"\nOr use the helper command (if added):\n"
            f"  python spotify_playlist_builder.py --store-credentials"
        )

    return client_id, client_secret


def store_credentials_in_keyring(client_id, client_secret, service="spotify-playlist-builder"):
    """Store credentials in macOS Keychain (or OS credential store)."""
    if not KEYRING_AVAILABLE:
        raise Exception("keyring library not available")

    keyring.set_password(service, "client_id", client_id)
    keyring.set_password(service, "client_secret", client_secret)
    print(f"✓ Credentials stored securely in {keyring.get_keyring().__class__.__name__}")


def get_credentials(source="env", vault="Private", item="SpotifyPlaylistBuilder"):
    """
    Get Spotify credentials from specified source.

    Args:
        source: "env" for .env file, "keyring" for OS keychain, or "1password" for 1Password vault
        vault: 1Password vault name (default: Private)
        item: 1Password item name (default: SpotifyPlaylistBuilder)

    Returns:
        Tuple of (client_id, client_secret)
    """
    if source.lower() == "env":
        return get_credentials_from_env()
    elif source.lower() == "keyring":
        return get_credentials_from_keyring()
    elif source.lower() == "1password":
        return get_credentials_from_1password(vault, item)
    else:
        raise ValueError(f"Unknown credential source: {source}. Use 'env', 'keyring', or '1password'")


# Spotify Playlist Builder Class
class SpotifyPlaylistBuilder:
    def __init__(self, client_id, client_secret, redirect_uri="https://127.0.0.1:8888/callback"):
        """Initialize Spotify API client with OAuth authentication."""
        scope = "playlist-modify-public playlist-modify-private"
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope,
                open_browser=True
            )
        )
        # Get the current authenticated user's ID
        self.user_id = self.sp.current_user()['id']

    def search_track(self, artist, track, album=None):
        """
        Search for a track on Spotify, return URI if found.

        Args:
            artist: Artist name
            track: Track name
            album: Optional album name to prefer

        Returns:
            Spotify URI if found, None otherwise
        """
        # If album is specified, try searching with album first
        if album:
            query = f"track:{track} artist:{artist} album:{album}"
            results = self.sp.search(q=query, type="track", limit=5)

            if results["tracks"]["items"]:
                # Find exact album match if possible
                for item in results["tracks"]["items"]:
                    if album.lower() in item["album"]["name"].lower():
                        return item["uri"]
                # If no exact match, use first result from album search
                return results["tracks"]["items"][0]["uri"]

        # Fallback: search without album, prefer studio albums over compilations
        query = f"track:{track} artist:{artist}"
        results = self.sp.search(q=query, type="track", limit=10)

        if results["tracks"]["items"]:
            # Try to avoid compilations/greatest hits
            compilation_keywords = ["greatest hits", "best of", "collection", "singles", "anthology", "essential", "electrospective", "retrospective"]

            # First pass: look for non-compilation albums
            for item in results["tracks"]["items"]:
                album_name = item["album"]["name"].lower()
                if not any(keyword in album_name for keyword in compilation_keywords):
                    return item["uri"]

            # If all are compilations, just return the first result
            return results["tracks"]["items"][0]["uri"]

        return None

    def find_playlist_by_name(self, playlist_name):
        """Find a playlist by name for the authenticated user."""
        offset = 0
        limit = 50

        while True:
            playlists = self.sp.current_user_playlists(limit=limit, offset=offset)

            for playlist in playlists['items']:
                if playlist['name'] == playlist_name and playlist['owner']['id'] == self.user_id:
                    return playlist['id']

            if not playlists['next']:
                break
            offset += limit

        return None

    def get_playlist_tracks(self, playlist_id):
        """Get all track URIs from a playlist."""
        tracks = []
        offset = 0
        limit = 100

        while True:
            results = self.sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
            tracks.extend([item['track']['uri'] for item in results['items'] if item['track']])

            if not results['next']:
                break
            offset += limit

        return tracks

    def clear_playlist(self, playlist_id):
        """Remove all tracks from a playlist."""
        track_uris = self.get_playlist_tracks(playlist_id)

        # Remove in batches of 100 (Spotify API limit)
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i+100]
            self.sp.playlist_remove_all_occurrences_of_items(playlist_id, batch)

    def create_playlist(self, playlist_name, description=""):
        """Create a new playlist for the authenticated user."""
        playlist = self.sp.user_playlist_create(
            user=self.user_id,
            name=playlist_name,
            public=True,
            description=description
        )
        return playlist["id"]

    def _add_track_uris_to_playlist(self, playlist_id, track_uris):
        """Add track URIs to a playlist in batches."""
        # Add in batches of 100 (Spotify API limit)
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i+100]
            self.sp.playlist_add_items(playlist_id, batch)

    def add_tracks_to_playlist(self, playlist_id, tracks):
        """Add tracks to a playlist, handling batch operations."""
        uris = []
        failed_tracks = []

        for i, track in enumerate(tracks):
            artist = track.get("artist")
            track_name = track.get("track")
            album = track.get("album")  # Optional album field
            uri = self.search_track(artist, track_name, album)

            if uri:
                uris.append(uri)
            else:
                failed_tracks.append(f"{artist} - {track_name}")

            # Add in batches of 100 (Spotify API limit)
            if len(uris) == 100 or i == len(tracks) - 1:
                if uris:
                    self.sp.playlist_add_items(playlist_id, uris)
                    uris = []

        return failed_tracks

    def build_playlist_from_json(self, json_file):
        """Build or update a playlist from a JSON file."""
        with open(json_file, "r") as f:
            playlist_data = json.load(f)

        playlist_name = playlist_data.get("name", "New Playlist")
        description = playlist_data.get("description", "")
        tracks = playlist_data.get("tracks", [])

        print(f"Authenticated as: {self.user_id}")
        print(f"Processing playlist: {playlist_name}")

        # Search for tracks with updated logic (prefer studio albums)
        print(f"Searching for {len(tracks)} tracks (preferring studio albums)...")
        new_track_uris = []
        failed_tracks = []

        for track in tracks:
            artist = track.get("artist")
            track_name = track.get("track")
            album = track.get("album")
            uri = self.search_track(artist, track_name, album)

            if uri:
                new_track_uris.append(uri)
            else:
                failed_tracks.append(f"{artist} - {track_name}")

        # Check if playlist already exists
        existing_playlist_id = self.find_playlist_by_name(playlist_name)

        if existing_playlist_id:
            print(f"Found existing playlist (ID: {existing_playlist_id})")
            current_track_uris = self.get_playlist_tracks(existing_playlist_id)

            # Compare current tracks with new tracks
            if current_track_uris == new_track_uris:
                print("Playlist is already up to date, no changes needed.")
            else:
                print(f"Playlist needs updating (current: {len(current_track_uris)} tracks, new: {len(new_track_uris)} tracks)")
                print("Clearing existing tracks...")
                self.clear_playlist(existing_playlist_id)
                print("Adding updated tracks...")
                self._add_track_uris_to_playlist(existing_playlist_id, new_track_uris)
                print("✓ Playlist updated successfully!")

            playlist_id = existing_playlist_id
        else:
            print(f"Creating new playlist...")
            playlist_id = self.create_playlist(playlist_name, description)
            print(f"Playlist created (ID: {playlist_id})")
            print(f"Adding {len(new_track_uris)} tracks...")
            self._add_track_uris_to_playlist(playlist_id, new_track_uris)
            print("✓ Playlist created successfully!")

        if failed_tracks:
            print(f"\n⚠️  {len(failed_tracks)} tracks not found:")
            for track in failed_tracks:
                print(f"  - {track}")

        print(f"\nPlaylist ready: https://open.spotify.com/playlist/{playlist_id}")


# Main Execution
def main():
    # Handle --list-vaults command
    if "--list-vaults" in sys.argv:
        list_1password_vaults()
        return

    # Handle --store-credentials command
    if "--store-credentials" in sys.argv:
        print("Store Spotify credentials in macOS Keychain")
        client_id = input("Enter Spotify Client ID: ").strip()
        client_secret = input("Enter Spotify Client Secret: ").strip()

        if client_id and client_secret:
            try:
                store_credentials_in_keyring(client_id, client_secret)
                print("\nCredentials stored! You can now use: --source keyring")
            except Exception as e:
                print(f"Error storing credentials: {e}")
                sys.exit(1)
        else:
            print("Error: Both Client ID and Client Secret are required")
            sys.exit(1)
        return

    if len(sys.argv) < 2:
        print("Usage: python spotify_playlist_builder.py <json_file> [--source env|keyring|1password] [--vault VAULT_NAME]")
        print("\nExamples:")
        print("  python spotify_playlist_builder.py playlist.json")
        print("  python spotify_playlist_builder.py playlist.json --source keyring")
        print("  python spotify_playlist_builder.py playlist.json --source env")
        print("  python spotify_playlist_builder.py playlist.json --source 1password")
        print("  python spotify_playlist_builder.py playlist.json --source 1password --vault Personal")
        print("\nHelper commands:")
        print("  python spotify_playlist_builder.py --store-credentials  # Store credentials in macOS Keychain")
        print("  python spotify_playlist_builder.py --list-vaults        # List available 1Password vaults")
        print("\nNote: The playlist will be created for the authenticated Spotify user.")
        sys.exit(1)

    json_file = sys.argv[1]

    # Parse optional source argument
    source = "env"  # Default to .env
    if "--source" in sys.argv:
        source_idx = sys.argv.index("--source")
        if source_idx + 1 < len(sys.argv):
            source = sys.argv[source_idx + 1]

    # Parse optional vault argument (for 1Password)
    vault = "Private"  # Default vault
    if "--vault" in sys.argv:
        vault_idx = sys.argv.index("--vault")
        if vault_idx + 1 < len(sys.argv):
            vault = sys.argv[vault_idx + 1]

    # Validate inputs
    if not Path(json_file).exists():
        print(f"Error: {json_file} not found")
        sys.exit(1)

    try:
        # Get credentials from specified source
        if source.lower() == "1password":
            print(f"Fetching credentials from {source} (vault: {vault})...")
        else:
            print(f"Fetching credentials from {source}...")
        client_id, client_secret = get_credentials(source, vault=vault)

        # Build playlist
        builder = SpotifyPlaylistBuilder(client_id, client_secret)
        builder.build_playlist_from_json(json_file)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
