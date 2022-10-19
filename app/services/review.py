from typing import TYPE_CHECKING, Optional

from loguru import logger

from app.storage import schemas
from app.storage import cruds
from app.storage.session import session


if TYPE_CHECKING:
    from app.storage.models import Review


async def get_no_review_users_by_round(event_id: int, round: int) -> list[int]:
    """Get members w/o review by round.

    Args:
        event_id (int): Event row id.
        round (int): Round number.

    Returns:
        list[int]: List of telegram ids.
    """
    no_review = await cruds.review.get_no_review_by_round(session, event_id, round)
    return [review.author_id for review in no_review]
