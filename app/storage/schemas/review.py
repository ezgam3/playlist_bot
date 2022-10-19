from pydantic import BaseModel


class ReviewBase(BaseModel):
    author_id: int
    playlist_id: int
    rating: int
    comment: str


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    pass


class ReviewInDBBase(ReviewBase):
    id: int

    class Config:
        orm_mode = True


class Review(ReviewInDBBase):
    pass


class ReviewInDB(ReviewInDBBase):
    pass
