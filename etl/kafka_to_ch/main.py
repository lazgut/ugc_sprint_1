import asyncio
import random

from clickhouse_driver import connect
from kafka import KafkaProducer

from kafka_to_ch.helpers.backoff import backoff
from tools.extractor import KafkaExtractor
from tools.loader import ClickHouseLoader
from settings import Settings


@backoff()
async def main():
    settings = Settings()

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    for i in range(20):
        value = bytes(str(random.randrange(160000, 199999)), encoding='utf-8')

        # INPUT DATA
        producer.send(
            topic='views',
            value=value,
            key=b'953339a0-bc6c-4bbd-88d2-4ee7afae6ec9+10ebcaa3-279a-4b3d-9411-351ccf1746ab',
        )

    producer.close()

    kafka_point = KafkaExtractor('views',
                                 auto_offset_reset='earliest',
                                 bootstrap_servers='localhost:9092',
                                 enable_auto_commit=False,
                                 group_id='echo-messages-to-stdout',
                                 chunk_size=10000,
                                 consumer_timeout_ms=1000)

    with kafka_point as consumer, \
            connect('clickhouse://localhost') as conn_ch, conn_ch.cursor() as cursor:
        kafka_generator = kafka_point.extract_data()

        clickhouse_load = ClickHouseLoader(connect_ch=conn_ch, cursor=cursor, kafka_point=consumer)
        clickhouse_load.generate_data(kafka_generator)

        last_data = kafka_point.data_extract
        if last_data:
            clickhouse_load.insert_data(last_data)


if __name__ == '__main__':
    asyncio.run(main())
