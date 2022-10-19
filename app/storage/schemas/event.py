from datetime import datetime

from pydantic import BaseModel

from app.core.states import EventStates


class EventBase(BaseModel):
    name: str
    description: str
    rules: str
    start_date: datetime
    end_date: datetime | None = None
    state: int | EventStates
    round_duration: int | None = None
    members: list[int] = list()
    round: int | None = None
    playlist_queue: dict[int, int] | None = None


class EventCreate(EventBase):
    name: str
    state: EventStates = EventStates.COLLECT_PLAYLIST.value
    round: int = 0
    round_duration: int


class EventUpdate(EventBase):
    pass


class EventInDBBase(EventBase):
    id: int

    class Config:
        orm_mode = True


class Event(EventInDBBase):
    pass


class EventInDB(EventInDBBase):
    pass
