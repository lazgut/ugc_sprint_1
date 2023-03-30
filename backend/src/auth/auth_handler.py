import time
import uuid

import jwt
from core.config import settings


JWT_SECRET = settings.SECRET
JWT_ALGORITHM = settings.ALGORITHM


def is_valid_uuid4(val):
    try:
        uuid_obj = uuid.UUID(val)
        print("uuid_obj: ", uuid_obj)
    except ValueError:
        return False

    return str(uuid_obj) ==val

def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: uuid.UUID) -> dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # print("From sign - ", token)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print("From decode - ", decoded_token)
        return decoded_token if is_valid_uuid4(decoded_token["user_id"]) else None
    except:
        return {}

# #
# token = signJWT("d99cfebe-0f2c-4098-b5aa-b27229943f2b").get("access_token")
# print("user_id: ", "d99cfebe-0f2c-4098-b5aa-b27229943f2b", " ----- ", "access_token: ", token)
#
# user_id_test = decodeJWT(token)
# print("user_id: ", user_id_test)