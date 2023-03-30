from pydantic import BaseModel
from pydantic.types import UUID4


class View(BaseModel):
    film_id: UUID4
    topic: str
    value: int
