import uuid

from pydantic import BaseModel


class View(BaseModel):
    movie_uuid: uuid.UUID
    topic: str
    value: int
