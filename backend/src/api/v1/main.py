import logging
from http import HTTPStatus
from fastapi import HTTPException, APIRouter
from starlette.requests import Request
import orjson
from db.kafka_producer import get_aioproducer
from models.models import View


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/addview")
async def add_view(view: View, request: Request):
    """
    An example request JSON:
    {

    "movie_uuid": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    "topic": "views",
    "value": 3921837
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    user_uuid = request.headers.get('user_uuid')
    if not user_uuid:
        raise HTTPException(401, detail='Unauthorized')
    try:
        producer = await get_aioproducer()
        await producer.send(
             topic=view.topic,
             value=str(view.value).encode(),
             key=f'{user_uuid}+{view.movie_uuid}'.encode()
             )
        success = True
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success})

