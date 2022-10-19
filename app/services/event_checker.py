from typing import TYPE_CHECKING

from aiogram import Bot
from loguru import logger
import pendulum

from app.core import constants
from app.core.states import EventStates
from app.services import events, notification
from app.core.typdefs import TimeInterval

if TYPE_CHECKING:
    from app.storage.models import Event


async def event_checker(playlist_bot: Bot) -> None:
    """Check events."""
    logger.debug("Event checker")
    event = await events.get_current_event()
    if event is None:
        logger.debug("No current event")
        return
    round_interval = await events.get_current_round_time_interval(event)
    if await _check_event_start(event):
        await events.start_event(playlist_bot)
        return await notification.newsletter_playlists(playlist_bot, event)
    if await _check_round_end_soon(round_interval):
        return await notification.notify_about_round_end_soon(event)
    if await _check_round_change(event, round_interval):
        await events.change_round(event)
        return await notification.newsletter_playlists(playlist_bot, event)

    logger.debug("No triggers in event checker")


async def _check_event_start(event: "Event") -> bool:
    """Check event start."""
    logger.debug("Check event start")
    if event is None:
        return False

    if event.state != EventStates.COLLECT_PLAYLIST.value:
        return False

    if pendulum.instance(event.start_date, tz=constants.TIMEZONE) <= pendulum.now(
        tz=constants.TIMEZONE
    ):
        logger.debug("Time to start event.")
        return True

    return False


async def _check_round_end_soon(round_interval: TimeInterval) -> bool:
    """Check round end soon."""
    logger.debug("Check round end soon")

    if round_interval is None:
        return False

    if round_interval.end.subtract(minutes=constants.ROUND_END_SOON) <= pendulum.now(
        tz=constants.TIMEZONE
    ):
        return True

    return False


async def _check_round_change(event: "Event", round_interval: TimeInterval) -> bool:
    """Check if need a change round."""
    logger.debug("Check round change")

    if event is None:
        return False

    if event.state != EventStates.EVENT_IS_STARTED.value:
        return False

    if pendulum.now() >= round_interval.end:
        return True

    return False
