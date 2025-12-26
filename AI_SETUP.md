# Setting Up AI Features

The Spotify Playlist Builder uses **Google Gemini** to generate playlists based on your descriptions.
To use this feature, you need a free API Key from Google AI Studio.

## 1. Get a Gemini API Key

1. Go to **Google AI Studio**:
    [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account.
3. Click **"Create API key"**.
4. You can create a key in a new project or an existing Google Cloud project.
5. **Copy your API Key** immediately. You will need it for the next step.

> **Note:** The Gemini API has a generous free tier suitable for personal use. Check the
> [pricing page](https://ai.google.dev/pricing) for the latest details.

## 2. Configure the CLI

Once you have your key, run the following command in your terminal:

```bash
spotify-playlist-builder setup-ai
```

Paste your API key when prompted. The tool will securely store it in your system's keychain.

### Alternative: Environment Variable

If you prefer not to use the keychain or are running in a headless environment, you can set the
`GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Or add it to your `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

## 3. Test It Out

Verify your setup by generating a simple playlist:

```bash
spotify-playlist-builder generate --prompt "lo-fi coding beats"
```

If successful, you will see a JSON output of the generated tracks.
