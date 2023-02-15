import uuid
import random
import requests

def send_one_random():
    main_url = 'http://127.0.0.1:8000'
    url = f'{main_url}/v1/addview'
    obj = {"movie_uuid": str(uuid.uuid4()),
           "topic": "views",
           "value": random.randint(1, 10000000)
           }
    r = requests.post(url, json=obj, headers={'user_uuid': str(uuid.uuid4())})
    return r

if __name__ == '__main__':
    print(send_one_random().text)