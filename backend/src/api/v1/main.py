import orjson
from core.config import logger
from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def read_root():
    """
    Route for debug logs to ELK
    """
    logger.info("Пользователь вызвал hello world")
    return orjson.dumps({"Hello": "World"})
