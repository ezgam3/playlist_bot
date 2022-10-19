from typing import TYPE_CHECKING, Optional

import pendulum
from loguru import logger
from aiogram import Bot

from app.core.typdefs import TimeInterval
from app.core.states import EventStates
from app.core.distribution import distribute_playlists
from app.services import notification
from app.storage import schemas
from app.storage import cruds
from app.storage.session import session

if TYPE_CHECKING:
    from app.storage.models import Event


async def join_event(telegram_id: int, event_id: int) -> None:
    """Join event.

    Args:
        telegram_id (int): User telegram id.
        event_id (int): Event row id.
    """
    await cruds.event.add_event_member(session, event_id, telegram_id)


async def get_current_event() -> Optional["Event"]:
    """Get current event."""
    events = await cruds.event.get_multi(session, limit=1000)
    events = list(filter(_filter_event, events))
    if not events:
        return None
    else:
        return events[-1]


def _filter_event(event: "Event") -> bool:
    """Filter event."""
    return event.state == EventStates.COLLECT_PLAYLIST.value


async def create_event(
    name: str, description: str, rules: str, start_date: str, round_duration: int
) -> None:
    """Create event."""
    event = schemas.EventCreate(
        name=name,
        description=description,
        rules=rules,
        start_date=start_date,
        round_duration=round_duration,
    )
    await cruds.event.create(session, obj_in=event)


async def get_curent_event_members() -> list[int]:
    """Get current event members.

    Returns:
        list[int]: List of telegram ids.
    """
    event = await get_current_event()
    if not event:
        return []
    return event.members


async def get_current_event_state() -> Optional[EventStates]:
    """Get current event state."""
    event = await get_current_event()
    if not event:
        return None
    return EventStates(event.state)


async def change_state(event: "Event", state: EventStates) -> None:
    """Change event state."""
    await cruds.event.change_state(session, event.id, state.value)


async def start_event(playlist_bot: Bot) -> None:
    """Starting event."""
    event = await get_current_event()
    playlist_queue = distribute_playlists(event.members)
    await cruds.event.change_playlist_queue(session, event.id, playlist_queue)
    await notification.notify_users_about_event_start(playlist_bot, event)
    await change_state(event, EventStates.EVENT_IS_STARTED)
    await notification.newsletter_playlists(playlist_bot, event)

    logger.info('Event "{}" started', event.name)


async def get_current_round_time_interval(event: "Event") -> TimeInterval | None:
    """Get current round time interval.

    Args:
        event (Event): Event model.

    Returns:
        TimeInterval: Time interval.
    """
    if event is None:
        return None

    start_time = pendulum.instance(event.start_date)
    round_start_time = start_time.add(event.round * event.round_duration)
    round_end_time = round_start_time.add((event.round + 1) * event.round_duration)
    return TimeInterval(round_start_time, round_end_time)


async def change_round(event: "Event") -> None:
    """Change round."""
    round_count = len(event.members) - 1
    if event.round == round_count:
        await change_state(event, EventStates.EVENT_IS_ENDED)
        # TODO: notify end
    else:
        await cruds.event.change_round(session, event.id, event.round + 1)
        # TODO: notify next round
