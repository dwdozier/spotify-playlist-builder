from fastapi import FastAPI
from backend.app.api.v1.api import api_router

app = FastAPI(
    title="Spotify Playlist Builder API",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
