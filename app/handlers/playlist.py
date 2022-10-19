from aiogram import types

from app.entrypoint import dp
from app.core.states import UserStates, EventStates
from app.services import events, users, playlist


@dp.message_handler(commands="add")
async def add_playlist(message: types.Message) -> None:
    current_event = await events.get_current_event()
    if current_event is None:
        return await message.answer("😢Сейчас не проходит никаких событий.")

    if current_event.state != EventStates.COLLECT_PLAYLIST.value:
        return await message.answer("👓Событие уже началось, плейлисты нельзя добавлять.")

    if message.from_user.id not in current_event.members:
        return await message.answer("❌Вы не участник текущего события! (/join)")

    user = await users.get_user(message.from_user.id)
    await playlist.add_playlist(
        user_id=user.id, event_id=current_event.id, playlist_link=message.text
    )
    await users.change_state(user.telegram_id, UserStates.WAIT_BEGIN)
    await message.answer("✅Плейлист добавлен!")
