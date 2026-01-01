from sqladmin import ModelView, BaseView, expose
from starlette.responses import RedirectResponse
from sqlalchemy import select, func
from backend.app.models.user import User
from backend.app.models.playlist import Playlist
from backend.app.models.service_connection import ServiceConnection


class DashboardView(BaseView):
    name = "Dashboard"
    icon = "fa-solid fa-house"

    @expose("/", methods=["GET"])
    async def index(self, request):
        async with request.state.session as session:
            # Fetch simple stats
            user_count = await session.execute(select(func.count(User.id)))
            playlist_count = await session.execute(select(func.count(Playlist.id)))
            connection_count = await session.execute(select(func.count(ServiceConnection.id)))

            return await self.templates.TemplateResponse(
                request,
                "admin_dashboard.html",
                context={
                    "title": "VIB-O-MAT Control Center",
                    "description": (
                        "Welcome to the Series 2000 Administrative Interface. From here, you can "
                        "manage Citizens, monitor shared Playlists, and oversee Relay Station "
                        "connections."
                    ),
                    "stats": {
                        "users": user_count.scalar(),
                        "playlists": playlist_count.scalar(),
                        "connections": connection_count.scalar(),
                    },
                },
            )


class BackToAppView(BaseView):
    name = "Return to Vib-O-Mat"
    icon = "fa-solid fa-arrow-left"

    @expose("/exit", methods=["GET"])
    async def exit_admin(self, request):
        return RedirectResponse(url="/")


class UserAdmin(ModelView, model=User):
    column_list = ["id", "email", "is_active", "is_superuser", "is_verified", "is_public"]
    column_details_list = [
        "id",
        "email",
        "is_active",
        "is_superuser",
        "is_verified",
        "is_public",
        "favorite_artists",
        "unskippable_albums",
    ]
    form_columns = [
        "email",
        "is_active",
        "is_superuser",
        "is_verified",
        "is_public",
        "favorite_artists",
        "unskippable_albums",
    ]
    column_searchable_list = ["email"]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class PlaylistAdmin(ModelView, model=Playlist):
    column_list = ["id", "name", "user_id", "public"]
    column_searchable_list = ["name"]
    column_details_list = ["id", "name", "description", "public", "user_id", "source_id"]
    form_columns = ["name", "description", "public", "user_id", "source_id", "content_json"]
    name = "Playlist"
    name_plural = "Playlists"
    icon = "fa-solid fa-music"


class ServiceConnectionAdmin(ModelView, model=ServiceConnection):
    column_list = ["id", "provider_name", "user_id"]
    column_details_list = ["id", "provider_name", "provider_user_id", "user_id", "expires_at"]
    name = "Service Connection"
    name_plural = "Service Connections"
    icon = "fa-solid fa-link"
