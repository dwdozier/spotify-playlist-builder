import pytest
from backend.app.core.auth.manager import UserManager
from backend.app.models.user import User
from unittest.mock import MagicMock


@pytest.mark.asyncio
async def test_user_manager_on_after_register():
    """Test the on_after_register hook in UserManager."""
    mock_user_db = MagicMock()
    manager = UserManager(mock_user_db)
    user = User(email="test@example.com")

    # This currently just prints, but let's call it to cover the line
    await manager.on_after_register(user)
