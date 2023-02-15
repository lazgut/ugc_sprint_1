import random
import asyncio

import clickhouse_driver

connection_info = {
    'host': 'localhost',
    'port': 9000,
}

class Uuids:
    def __init__(self):
        with open('users') as fu:
            self.users = [s.strip() for s in fu.readlines()]
        with open('movies') as fm:
            self.movies = [s.strip() for s in fm.readlines()]

    @property
    def random_user(self):
        return self.users[random.randint(0, len(self.users)-1)]

    @property
    def random_movie(self):
        return self.movies[random.randint(0, len(self.movies)-1)]




def send_one_batch(uuids, cur):
    for i in range(100):
        print(i)
        sql = """INSERT INTO default.cinema_ch (id, event_time, topic) VALUES"""
        data = [(f'{uuids.random_user}+{uuids.random_movie}', str(random.randint(0, 1000000)), "views") for _ in range(10000)]

        cur.executemany(sql, data)


def main(count):
    uuids = Uuids()
    # async with aiovertica.connect(**connection_info) as connection:
    connection = clickhouse_driver.connect(**connection_info)
    cur = connection.cursor()

    for number in range(1):
        send_one_batch(uuids, cur)

        # await asyncio.gather(*tasks)

if __name__ == '__main__':
    main(10)