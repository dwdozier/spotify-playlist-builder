from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from backend.app.core.config import settings

SECRET = settings.SECRET_KEY


cookie_transport = CookieTransport(
    cookie_max_age=3600,
    cookie_samesite="lax",
    cookie_secure=False,  # Set to True in production with HTTPS
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
