from typing import TYPE_CHECKING, Optional

from loguru import logger

from app.storage import schemas
from app.storage import cruds
from app.storage.session import session
from app.core.states import UserStates

if TYPE_CHECKING:
    from app.storage.models import User


async def get_user_state(telegram_id: int) -> UserStates:
    """Get user state."""
    state = await cruds.user.get_state(session, telegram_id)
    return UserStates(state)


async def get_user(telegram_id: int) -> Optional["User"]:
    """Get user by telegram id."""
    return await cruds.user.get_by_telegram_id(session, telegram_id)


async def create_user(telegram_id: int) -> "User":
    """Create user."""
    logger.info("Create new user with telegram_id={}", telegram_id)
    user = schemas.UserCreate(telegram_id=telegram_id)
    return await cruds.user.create(session, obj_in=user)


async def change_state(telegram_id: int, state: UserStates) -> None:
    """Change user state."""
    logger.info("Change user state telegram_id={} to state={}", telegram_id, state)
    await cruds.user.change_state(session, telegram_id, state.value)
