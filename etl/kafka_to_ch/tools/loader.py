from typing import Generator

from clickhouse_driver.connection import Connection
from clickhouse_driver.dbapi.cursor import Cursor

from helpers.queries import QUERY_INSERT_INTO_CINEMA_CH


class ClickHouseLoader:
    def __init__(
        self,
        connect_ch: Connection,
        cursor: Cursor,
        query: str = QUERY_INSERT_INTO_CINEMA_CH,
    ):
        self.connect_ch = connect_ch
        self.cursor = cursor
        self.query = query

    def generate_data(self, generate_data: Generator):
        for chunk in generate_data:
            data_load = chunk
            self.insert_data(data_load)

    def insert_data(self, data: list):
        self.cursor.executemany(self.query, data)
        return
