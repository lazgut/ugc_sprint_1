import asyncio

from clickhouse_driver import connect

from helpers.backoff import backoff
from tools.extractor import KafkaExtractor
from tools.loader import ClickHouseLoader
from settings import Settings


@backoff()
async def main():
    settings = Settings()

    kafka_point = KafkaExtractor('views',
                                 auto_offset_reset=settings.offset_reset_ch,
                                 bootstrap_servers=settings.kafka_dsn,
                                 enable_auto_commit=settings.auto_commit_ch,
                                 group_id=settings.group_id_ch,
                                 chunk_size=settings.chunk_size_ch,
                                 consumer_timeout_ms=settings.consumer_timeout_ms_ch)

    with kafka_point as consumer, \
            connect(settings.clickhouse_dsn) as conn_ch, conn_ch.cursor() as cursor:
        kafka_generator = kafka_point.extract_data()

        clickhouse_load = ClickHouseLoader(connect_ch=conn_ch, cursor=cursor, kafka_point=consumer)
        clickhouse_load.generate_data(kafka_generator)

        last_data = kafka_point.data_extract
        if last_data:
            clickhouse_load.insert_data(last_data)


if __name__ == '__main__':
    while True:
        asyncio.run(main())
