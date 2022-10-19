from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from app.entrypoint import dp
from app.core import states
from app.core.states import UserStates
from app.services import events, users


@dp.message_handler(commands="join")
async def join_event(message: types.Message) -> None:
    """Join event."""
    state = await users.get_user_state(message.from_user.id)
    if state != UserStates.NO_EVENT:
        return await message.answer("Ты уже вступил в событие. (/event)")

    event = await events.get_current_event()
    if event is None:
        return await message.answer("😱Сейчас нет активных событий. Создай свое событие! (/create)")

    await events.join_event(message.from_user.id, event.id)
    await users.change_state(message.from_user.id, UserStates.ADD_PLAYLIST)
    await message.answer("🎉Ты вступил в событие. Теперь ты можешь добавить плейлист. (/add)")


@dp.message_handler(commands="create", state="*")
async def create_event_name(message: types.Message, state: FSMContext) -> None:
    event = await events.get_current_event()
    if event is not None:
        return await message.answer("😱Сейчас уже идет событие! Присоединяйся! (/join)")

    await message.answer("🎉Создай свое событие!\nНапиши название события:")
    await state.set_state(states.CreateEvent.name)


@dp.message_handler(state=states.CreateEvent.name)
async def create_event_description(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(states.CreateEvent.description)
    await message.answer("Напиши описание события:")


@dp.message_handler(state=states.CreateEvent.description)
async def create_event_rules(message: types.Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(states.CreateEvent.rules)
    await message.answer("Напиши правила события:")


@dp.message_handler(state=states.CreateEvent.rules)
async def create_event_start_date(message: types.Message, state: FSMContext) -> None:
    await state.update_data(rules=message.text)
    await state.set_state(states.CreateEvent.start_date)
    await message.answer("Напиши дату начала события в формате DD.MM.YYYY HH:MM:")


@dp.message_handler(state=states.CreateEvent.start_date)
async def create_event_start_time(message: types.Message, state: FSMContext) -> None:
    start_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    await state.update_data(start_date=start_time)
    await state.set_state(states.CreateEvent.round_duration)
    await message.answer("Напиши продолжительность раунда в часах:")


@dp.message_handler(state=states.CreateEvent.round_duration)
async def create_event_finish(message: types.Message, state: FSMContext) -> None:
    await state.update_data(round_duration=message.text)
    data = await state.get_data()
    await message.answer(
        f"""Давай проверим, что у нас получилось в итоге.
Название: {data.get('name')}
Описание: {data.get('description')}
Правила: {data.get('rules')}
Дата начала: {data.get('start_date')}
Длительность раунда: {data.get('round_duration')}"""
    )
    await events.create_event(**data)
    await state.finish()
    await message.answer("🎉Событие создано!")


# TODO: Добавить возможность отредактировать данные, либо просто отказаться от создания
# Гайд про автоматы - https://mastergroosha.github.io/aiogram-2-guide/fsm/
