from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.clients.microsoft import MicrosoftGraphOAuth2
from httpx_oauth.oauth2 import BaseOAuth2
from backend.app.core.config import settings


# Note: Apple requires a custom client_secret generation (JWT signed with .p8 key)
# which is not standard OAuth2. This is a placeholder for the endpoint.
class AppleOAuth2(BaseOAuth2):
    def __init__(self, client_id, client_secret):
        super().__init__(
            client_id,
            client_secret,
            "https://appleid.apple.com/auth/authorize",
            "https://appleid.apple.com/auth/token",
            name="apple",
        )


google_oauth_client = GoogleOAuth2(
    settings.GOOGLE_OAUTH_CLIENT_ID or "",
    settings.GOOGLE_OAUTH_CLIENT_SECRET or "",
)

github_oauth_client = GitHubOAuth2(
    settings.GITHUB_OAUTH_CLIENT_ID or "",
    settings.GITHUB_OAUTH_CLIENT_SECRET or "",
)

# TODO: Add Microsoft OAuth credentials to settings
microsoft_oauth_client = MicrosoftGraphOAuth2(
    "",
    "",
)

# TODO: Add Apple OAuth credentials to settings
apple_oauth_client = AppleOAuth2(
    "",
    "",
)
