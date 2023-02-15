import asyncio
import random
import uuid
import requests

import aiohttp
from subprocess import Popen, PIPE


def send_one_random():
    main_url = 'http://127.0.0.1:8000'
    url = f'{main_url}/v1/addview'
    obj = {"movie_uuid": str(uuid.uuid4()),
           "topic": "views",
           "value": random.randint(1, 10000000)
           }
    r = requests.post(url, json=obj, headers={'user_uuid': str(uuid.uuid4())})
    return r


async def send_one_async(session, url):

    obj = {"movie_uuid": str(uuid.uuid4()),
           "topic": "views",
           "value": random.randint(1, 10000000)
           }

    async with session.post(url, json=obj, headers={'user_uuid': str(uuid.uuid4())}) as resp:
        result = await resp.text()
        return result


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for number in range(100000):
            main_url = 'http://127.0.0.1:8000'
            url = f'{main_url}/v1/addview'
            tasks.append(send_one_async(session, url))

        gathered = await asyncio.gather(*tasks)
        for one in gathered:
            print(one)


def ask_records_count():
    sql_cmd = 'SELECT COUNT(*) FROM cinema_ch'
    docker_cmd = f'echo "{sql_cmd}" | clickhouse-client'
    here_cmd = f"-ti clickhouse-node1 bash -c '{docker_cmd}'"
    print(here_cmd)
    with open('out', 'w') as outfile:
        proc = Popen(args=['docker', 'exec', 'clickhouse-node1', 'bash', '-c', docker_cmd], stdout=PIPE)
        # proc.wait()
    #stdout = proc.communicate()[0]
    result = proc.stdout.read()
    return int(result)


if __name__ == '__main__':
    # asyncio.run(main())
    print(ask_records_count())