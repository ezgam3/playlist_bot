from pydantic import BaseModel


class UserBase(BaseModel):
    telegram_id: int | None = None
    state: int | None = None
    is_admin: bool = False
    is_member: bool = False


class UserCreate(UserBase):
    telegram_id: int
    state: int = 0


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass
