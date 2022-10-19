from pydantic import BaseModel


class PlaylistBase(BaseModel):
    telegram_id: int
    event_id: int
    link: str
    description: str | None = None


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistUpdate(PlaylistBase):
    pass


class PlaylistInDBBase(PlaylistBase):
    id: int

    class Config:
        orm_mode = True


class Playlist(PlaylistInDBBase):
    pass


class PlaylistInDB(PlaylistInDBBase):
    pass
