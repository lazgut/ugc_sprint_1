"""
Requirements:
confluent-kafka=2.0.2
faker=16.8.1
"""
from confluent_kafka import Producer  # Producer  # confluent_kafka
from faker import Faker
import json
import time
import logging
import random

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='../producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

fake=Faker()

p1=Producer({'bootstrap.servers':'localhost:9092'})
p2=Producer({'bootstrap.servers':'localhost:9093'})
p3=Producer({'bootstrap.servers':'localhost:9094'})
producers = [p1, p2, p3]
print('Kafka Producer has been initiated...')


def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)


def main():
    for i in range(10):
        data={
           'user_id': fake.random_int(min=20000, max=100000),
           'user_name':fake.name(),
           'user_address':fake.street_address() + ' | ' + fake.city() + ' | ' + fake.country_code(),
           'platform': random.choice(['Mobile', 'Laptop', 'Tablet']),
           'signup_at': str(fake.date_time_this_month())
           }
        producer_number = i % len(producers)
        p = producers[producer_number]
        m=json.dumps(data)
        p.poll(1)
        p.produce('user-tracker', m.encode('utf-8'),callback=receipt)
        p.flush()
        time.sleep(3)

if __name__ == '__main__':
    main()