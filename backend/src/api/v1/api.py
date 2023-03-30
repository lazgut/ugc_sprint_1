import logging
from http import HTTPStatus
import uuid

from fastapi import APIRouter, Depends, HTTPException
import orjson

from db.kafka_producer import get_aioproducer
from models.view import View
from auth.auth_handler import signJWT
from auth.auth_bearer import get_current_user_id


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/login",
    status_code=200
)
def login(user_id: uuid.UUID):
    access_token = signJWT(str(user_id))
    # except Exception as e:
    #     logger.error(e)
    #     raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps(access_token)


@router.post(
    "/add_view",
    status_code=201,
    responses={403: {"description": "Could not validate credentials"}},
    summary="Recording movie viewing progress",
    description="Records the progress of the user's movie viewing ",
)
async def add_view(view: View, user_id: uuid.UUID = Depends(get_current_user_id)):
    try:
        producer = await get_aioproducer()
        await producer.send(
            topic=view.topic,
            value=str(view.value).encode(),
            key=f'{user_id}+{view.film_id}'.encode()
        )
        success = True
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success})