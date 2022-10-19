from enum import Enum

from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(Enum):
    NO_EVENT = 0
    ADD_PLAYLIST = 1
    WAIT_BEGIN = 2
    LISTINING_PLAYLIST = 3
    ADD_REVIEW = 4
    WAITING_NEXT_PLAYLIST = 5
    WAIT_EVERYONE = 6


class EventStates(Enum):
    COLLECT_PLAYLIST = 0
    EVENT_IS_STARTED = 1
    EVENT_IS_ENDED = 2


class CreateEvent(StatesGroup):
    name = State()
    description = State()
    rules = State()
    start_date = State()
    round_duration = State()
