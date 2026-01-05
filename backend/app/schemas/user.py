import uuid
from typing import List, Any, Optional
from pydantic import BaseModel, ConfigDict
from fastapi_users import schemas


class ServiceConnectionRead(BaseModel):
    provider_name: str
    is_connected: bool
    client_id: Optional[str] = None
    has_secret: bool = False
    scopes: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class UserRead(schemas.BaseUser[uuid.UUID]):
    is_public: bool
    favorite_artists: List[Any]
    unskippable_albums: List[Any]
    service_connections: List[ServiceConnectionRead] = []


class UserCreate(schemas.BaseUserCreate):
    is_public: bool = True
    favorite_artists: List[Any] = []
    unskippable_albums: List[Any] = []


class UserUpdate(schemas.BaseUserUpdate):
    is_public: Optional[bool] = None
    favorite_artists: Optional[List[Any]] = None
    unskippable_albums: Optional[List[Any]] = None


class UserPublic(BaseModel):
    id: uuid.UUID
    email: str  # We might want to mask this in a real app
    favorite_artists: List[Any]
    unskippable_albums: List[Any]
    is_public: bool

    model_config = ConfigDict(from_attributes=True)
