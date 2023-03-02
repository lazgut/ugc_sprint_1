import uuid

from pydantic import BaseModel

# No need to pass 'user' here, this is for FastApi, user uuid goes
# from the request header.


class Movie(BaseModel):
    id: uuid.UUID


class Like(BaseModel):
    movie: uuid.UUID
    # user: uuid.UUID
    value: int  # 0-10


class Review(BaseModel):
    movie: uuid.UUID
    # user: uuid.UUID
    text: str


class ReviewId(BaseModel):
    id: uuid.UUID


class ReviewLike(BaseModel):
    movie: uuid.UUID
    review: str
    # user: uuid.UUID
    value: int  # 0-10


class Bookmark(BaseModel):
    movie: uuid.UUID
    # user: uuid.UUID
