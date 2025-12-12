---
description: Verify Python environment, dependencies, and project setup
---

Run a comprehensive check of the development environment and dependencies for this project.

Check the following:

1. **Python Version**: Verify Python 3.11+ is available
   - Run: `python --version` or `python3 --version`

2. **UV Package Manager**: Verify uv is installed
   - Run: `uv --version`

3. **Virtual Environment**: Check if .venv exists and is properly configured
   - Check: `.venv` directory exists
   - Run: `source .venv/bin/activate && python -c "import sys; print(sys.prefix)"`

4. **Dependencies**: Verify all required packages are installed
   - Run: `.venv/bin/python -c "import spotipy, dotenv; print('Dependencies OK')"`

5. **Credentials**: Check if credentials are configured (without displaying them)
   - Check: `.env` file exists OR 1Password CLI is available (`which op`)

6. **Project Files**: Verify core files exist
   - Check: `spotify_playlist_builder.py`, `pyproject.toml`, `playlists/` directory

Provide a clear summary of what's working and what needs attention. If something is missing, provide instructions on how to fix it.
