import os
import json
import asyncio
import random
from time import sleep

from clickhouse_driver import Client, connect
from kafka import KafkaProducer, KafkaConsumer

from etl.kafka_to_ch.settings import Settings


async def main():
    settings = Settings()

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    for i in range(100):
        value = bytes(str(random.randrange(160000, 199999)), encoding='utf-8')

        # INPUT DATA
        producer.send(
            topic='views',
            value=value,
            key=b'953339a0-bc6c-4bbd-88d2-4ee7afae6ec9+10ebcaa3-279a-4b3d-9411-351ccf1746ab',
        )

    producer.close()

    consumer = KafkaConsumer('views',
                             auto_offset_reset='earliest',
                             group_id='echo-messages-to-stdout',
                             bootstrap_servers=['localhost:9092'],
                             enable_auto_commit=False,
                             consumer_timeout_ms=1000,
                             value_deserializer=lambda m: json.loads(m.decode('ascii')))
    count = 0
    data = []

    for message in consumer:
        if count >= 10:
            break
        cash_data = []
        count += 1
        cash_data.append(message.key)
        cash_data.append(message.value)
        cash_data.append(message.topic)
        data.append(cash_data)



    pass
    #
    # client = Client(host='localhost')
    conn = connect('clickhouse://localhost')
    cursor = conn.cursor()

    cursor.execute('CREATE DATABASE IF NOT EXISTS test ON CLUSTER company_cluster')
    create = cursor.execute(
        'CREATE TABLE IF NOT EXISTS test.regular_table ON CLUSTER company_cluster (id String, event_time Int32, topic String) Engine=MergeTree() ORDER BY id')

    cursor.executemany('INSERT INTO test.regular_table (id, event_time, topic) VALUES', data)
    s = cursor.execute('SELECT * FROM test.regular_table')
    s = cursor.fetchall()

    # cursor.execute('DROP TABLE test.regular_table')


    # delete = client.execute('DROP TABLE test.regular_table')

    consumer.commit()
    pass


if __name__ == '__main__':
    asyncio.run(main())
