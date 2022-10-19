from typing import TYPE_CHECKING

from loguru import logger

from app.storage import schemas
from app.storage import cruds
from app.storage.session import session
from app.core.typdefs import PlaylistData

if TYPE_CHECKING:
    from app.storage.models import Playlist, Event


async def add_playlist(
    telegram_id: int, event_id: int, playlist_link: str, description: str | None = None
) -> None:
    """Add playlist to event.

    Args:
        user_id (int): User row id.
        event_id (int): Event row id.
        playlist_link (str): Playlist link.
        description (str, optional): Playlist description. Defaults to None.
    """
    playlist_data = schemas.PlaylistCreate(
        event_id=event_id,
        owner_id=telegram_id,
        link=playlist_link,
        description=description,
    )
    await cruds.playlist.create(session, obj_in=playlist_data)
    logger.info("Add playlist telegram_id={} to event_id={}", telegram_id, event_id)


# TODO: Добавить возможность редактировать плейлист


async def get_playlist(telegram_id: int) -> "Playlist":
    """Get playlist by telegram id.

    Args:
        telegram_id (int): Telegram id.

    Returns:
        Playlist: Playlist object.
    """
    logger.info("Get playlist by telegram_id={}", telegram_id)
    return await cruds.playlist.get_by_telegram_id(session, telegram_id=telegram_id)


async def get_round_playlist(event: "Event") -> dict[int, PlaylistData]:
    """Get round playlist.

    Args:
        event (Event): Event model.

    Returns:
        dict[int, int]: Dict of telegram ids with telegram ids whose playlist hear.
    """
    result = {}
    for k, v in event.playlist_queue.items():
        playlist = await get_playlist(v[event.round])
        owner_info = await cruds.user.get_by_telegram_id(session, playlist.owner_id)
        result[k] = PlaylistData(
            author_name=owner_info.name,
            author_telegram_id=owner_info.telegram_id,
            link=playlist.link,
            description=playlist.description,
        )
    return result
