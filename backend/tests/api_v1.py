"""Integration tests with launched services"""
import json
from unittest import TestCase

import requests


class Likes(TestCase):
    def setUp(self) -> None:
        # users_file = '../investigation/users'
        # movies_file = '../investigation/movies'
        # with open(users_file) as fu:
        #     self.users = [s.strip() for s in fu.readlines()]
        # with open(movies_file) as fm:
        #     self.movies = [s.strip() for s in fm.readlines()]
        self.host_port = "127.0.0.1:8000"

    def test_add_like(self):
        result = requests.post(
            f"http://{self.host_port}/v1/likes/add",
            headers={"user_uuid": "d99cfebe-0f2c-4098-b5aa-b27229943f2b"},
            json={"movie": "391ae61e-5bce-41f8-b01a-9238c7831f21", "value": 3},
        )
        self.assertEqual(result.status_code, 200)
        obj = json.loads(result.json())
        self.assertTrue(obj["success"])

    def test_remove_like(self):
        result = requests.post(
            f"http://{self.host_port}/v1/likes/remove",
            headers={"user_uuid": "d99cfebe-0f2c-4098-b5aa-b27229943f2b"},
            json={
                "id": "391ae61e-5bce-41f8-b01a-9238c7831f21",
            },
        )
        self.assertEqual(result.status_code, 200)
        obj = json.loads(result.json())
        self.assertTrue(obj["success"])
