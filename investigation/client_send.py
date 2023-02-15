import asyncio
import random
import uuid
import requests

import aiohttp
from subprocess import Popen, PIPE
from time import sleep, time

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

def send_one_random():
    main_url = 'http://127.0.0.1:8000'
    url = f'{main_url}/v1/addview'
    obj = {"movie_uuid": str(uuid.uuid4()),
           "topic": "views",
           "value": random.randint(1, 10000000)
           }
    r = requests.post(url, json=obj, headers={'user_uuid': str(uuid.uuid4())})
    return r


async def send_one_async(uuids, session, url):

    obj = {"movie_uuid": uuids.random_movie,
           "topic": "views",
           "value": random.randint(1, 10000000)
           }

    async with session.post(url, json=obj, headers={'user_uuid': uuids.random_user}) as resp:
        result = await resp.text()
        return result


async def main(count):
    uuids = Uuids()
    async with aiohttp.ClientSession() as session:

        tasks = []
        for number in range(count):
            main_url = 'http://127.0.0.1:8000'
            url = f'{main_url}/v1/addview'
            tasks.append(send_one_async(uuids, session, url))

        gathered = await asyncio.gather(*tasks)
        for idx, one in enumerate(gathered):
            if idx % 1000 == 0:
                print(one, end=' ')
        print()
        print()


def ask_records_count():
    sql_cmd = 'SELECT COUNT(*) FROM cinema_ch'
    docker_cmd = f'echo "{sql_cmd}" | clickhouse-client'
    here_cmd = f"-ti clickhouse-node1 bash -c '{docker_cmd}'"
    proc = Popen(args=['docker', 'exec', 'clickhouse-node1', 'bash', '-c', docker_cmd], stdout=PIPE)

    result = proc.stdout.read()
    return int(result)


def report_records_count(start_time, first_record_count, limit):
    prev_record_count = None
    curr_record_count = first_record_count
    while curr_record_count - first_record_count < limit:
        sleep(1)
        curr_record_count = ask_records_count()
        if curr_record_count != prev_record_count:
            print("\ttime", time()-start_time, "\trecords", curr_record_count)
        prev_record_count = curr_record_count


if __name__ == '__main__':
    for i in range(1, 500):
        # print(i)
        count = 100000
        start_time = time()
        print(f'*** {i} ***')
        # print("start", start_time)
        first = ask_records_count()
        asyncio.run(main(count))

        # report_records_count(start_time, first, count)
    # u = Uuids()
    # print(u.random_user)
    # print(u.random_movie)