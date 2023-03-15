import orjson
from fastapi import APIRouter

from core.config import logger

router = APIRouter()


@router.get("/hello")
async def read_root():
    """
    Route for debug logs to ELK
    """
    logger.info("Пользователь вызвал hello world")
    return orjson.dumps({"Hello": "World"})
