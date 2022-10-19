from aiogram import types

from app.entrypoint import dp
from app.services import users
from app.services import events


@dp.message_handler(commands="start")
async def send_welcome(message: types.Message) -> None:
    user = await users.get_user(message.from_user.id)
    if user is None:
        await users.create_user(message.from_user.id)
        await message.answer(
            "👻Привет! Я бот, который поможет тебе обменяться плейлистами с твоими друзьями!"
        )
    event = await events.get_current_event()
    if event is not None:
        await message.answer(f"🎉Сейчас проходит событие {event.name}! Присоединяйся! (/join) ")
    else:
        await message.answer("😱Сейчас нет активных событий. Создай свое событие! (/create)")


@dp.message_handler(commands="test")
async def test(message: types.Message) -> None:
    await message.answer(await events.get_curent_event_members())
