from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship
from typing import List, TYPE_CHECKING
from backend.app.db.session import Base

if TYPE_CHECKING:
    from .service_connection import ServiceConnection
    from .playlist import Playlist


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    # Relationships
    service_connections: Mapped[List["ServiceConnection"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    playlists: Mapped[List["Playlist"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
