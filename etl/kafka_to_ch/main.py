import asyncio
import logging

from clickhouse_driver import connect
from helpers.backoff import backoff
from settings import Settings
from tools.extractor import KafkaExtractor
from tools.loader import ClickHouseLoader


@backoff()
async def main():
    logging.info("Created settings.")
    settings = Settings()

    kafka_point = KafkaExtractor(
        settings.topic_ch,
        auto_offset_reset=settings.offset_reset_ch,
        bootstrap_servers=settings.kafka_dsn,
        enable_auto_commit=settings.auto_commit_ch,
        group_id=settings.group_id_ch,
        chunk_size=settings.chunk_size_ch,
        consumer_timeout_ms=settings.consumer_timeout_ms_ch,
    )

    logging.info("Created kafka_point.")

    with kafka_point as consumer, connect(settings.clickhouse_dsn) as conn_ch, conn_ch.cursor() as cursor:
        logging.info("Extract data from Kafka")
        kafka_generator = kafka_point.extract_data()

        clickhouse_load = ClickHouseLoader(connect_ch=conn_ch, cursor=cursor)
        clickhouse_load.generate_data(kafka_generator)
        consumer.commit()
        logging.info("Data successful load to Clickhouse")

        last_data = kafka_point.data_extract
        if last_data:
            clickhouse_load.insert_data(last_data)
            consumer.commit()


if __name__ == "__main__":
    while True:
        logging.info("Start application")
        asyncio.run(main())
