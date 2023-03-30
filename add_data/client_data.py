import json
import random
import uuid

import orjson
import requests


def client_login(user_id: uuid.UUID) -> str:
    r = requests.post("http://0.0.0.0:8000/v1/login", params={"user_id": user_id})
    json_response: dict = orjson.loads(r.json())
    return json_response["access_token"]


def client_add_view(data: dict, token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    r = requests.post("http://0.0.0.0:8000/v1/add_view", json=data, headers=headers)
    print(r.status_code)
    print(r.request.body)


if __name__ == "__main__":
    for count in range(1000):
        access_token = client_login(uuid.uuid4())
        random_data = {
            "film_id": str(uuid.uuid4()),
            "topic": "views",
            "value": random.randint(0, 10000)
        }
        client_add_view(random_data, access_token)

        if count % 100 == 0:
            print(f"Записано - {count} событий")
