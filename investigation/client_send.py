import asyncio
import random
import uuid
import requests

import aiohttp


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
        for number in range(1, 151):
            main_url = 'http://127.0.0.1:8000'
            url = f'{main_url}/v1/addview'
            tasks.append(send_one_async(session, url))

        gathered = await asyncio.gather(*tasks)
        for one in gathered:
            print(one)


if __name__ == '__main__':
    asyncio.run(main())