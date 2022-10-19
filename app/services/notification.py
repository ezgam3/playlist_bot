from typing import TYPE_CHECKING

from aiogram import Bot

from app.core import constants
from app.core.typdefs import PlaylistData
from app.services import review, playlist

if TYPE_CHECKING:
    from app.storage.models import Event


async def notify_users(playlist_bot: Bot, telegram_ids: list[int], message: str) -> None:
    """Send message users.

    Args:
        telegram_ids (list[int]): List of telegram ids komy send a message.
        message (str): Message text.
    """
    for telegram_id in telegram_ids:
        await playlist_bot.send_message(telegram_id, message)


async def notify_users_about_event_start(playlist_bot: Bot, event: "Event") -> None:
    """Notify users about event start."""
    message = (
        f"🎉Событие {event.name} началось!\n"
        f"📝Описание: {event.description}\n"
        f"📅Дата начала: {event.start_date}\n"
        f"📜Правила: {event.rules}"
    )
    await notify_users(playlist_bot, event.members, message)


async def notify_users_about_new_round(playlist_bot: Bot, event: "Event") -> None:
    """Notify users about new round."""
    message = f"🎉Новый раунд! Раунд №{event.round}"
    await notify_users(event.members, message)


async def notify_users_unique_message(
    playlist_bot: Bot, telegram_ids_messages: dict[int, str]
) -> None:
    """Send unique message to users.

    Args:
        telegram_ids_messages (dict[int, str]): Dict of telegram ids and messages.
    """
    for telegram_id, message in telegram_ids_messages.items():
        await playlist_bot.send_message(telegram_id, message)


async def newsletter_playlists(playlist_bot: Bot, event: "Event") -> None:
    """newsletter playlists."""
    playlist_queue = await playlist.get_round_playlist(event)
    message = """Вот твой плейлист на этот раунд!
Ссылка: {link}
Описания плейлиста: {description}
© {author}
    """
    for telegram_id, playlist_data in playlist_queue.items():
        await playlist.send_message(
            telegram_id,
            message.format(
                link=playlist_data.link,
                description=playlist_data.description,
                author=playlist_data.author_name,
            ),
        )


async def notify_about_round_end_soon(playlist_bot: Bot, event: "Event") -> None:
    """Notify users about round end soon."""
    members_no_review = await review.get_no_review_users_by_round(event.id, event.round)
    message = f"""🕒Осталось меньше {constants.ROUND_END_SOON} минут до конца раунда!
Ты все еще не оставил отзыв! (Ты сможешь оставить его и позже, но не стоит откладывать на потом)
    """
    await notify_users(members_no_review, message)
