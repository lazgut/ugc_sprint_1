import random
import asyncio

import clickhouse_driver

connection_info = {
    'host': '127.0.0.1',
    'port': 8123,
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




async def send_one_async(uuids, cur):
    for i in range(100):
        print(i)
        sql = """INSERT INTO default.cinema_ch (id, event_time, topic) VALUES"""
        data = [(uuids.random_user, uuids.random_movie, random.randint(0, 1000000)) for _ in range(100000)]
        # sql2 = sql % (data[0])
        # print(sql, data)
        await cur.executemany(sql, data)


async def main(count):
    uuids = Uuids()
    # async with aiovertica.connect(**connection_info) as connection:
    with clickhouse_driver.connect(**connection_info) as connection:
        cur = connection.cursor()
        tasks = []
        for number in range(1):
            tasks.append(send_one_async(uuids, cur))

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main(10))