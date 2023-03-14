import uuid

from .common import BaseOrjsonModel

# No need to pass 'user' here, this is for FastApi, user uuid comes
# from the request header.


class Movie(BaseOrjsonModel):
    id: uuid.UUID


class Like(BaseOrjsonModel):
    movie: uuid.UUID
    value: int  # 0-10


class Review(BaseOrjsonModel):
    movie: uuid.UUID
    # user: uuid.UUID
    text: str


class ReviewId(BaseOrjsonModel):
    id: uuid.UUID


class ReviewLike(BaseOrjsonModel):
    movie: uuid.UUID
    review: str
    review_author_id: uuid.UUID
    value: int  # 0-10


class Bookmark(BaseOrjsonModel):
    movie: uuid.UUID
    # user: uuid.UUID
