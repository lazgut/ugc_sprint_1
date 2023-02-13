import uuid

from pydantic import BaseModel


class View(BaseModel):
    user_uuid: uuid.UUID
    movie_uuid: uuid.UUID
    topic: str
    value: int
