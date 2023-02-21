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
        topic=settings.TOPIC_CH,
        auto_offset_reset=settings.OFFSET_RESET_CH,
        bootstrap_servers=settings.KAFKA_DSN,
        enable_auto_commit=settings.AUTO_COMMIT_CH,
        group_id=settings.GROUP_ID_CH,
        chunk_size=settings.CHUNK_SIZE_CH,
        consumer_timeout_ms=settings.CONSUMER_TIMEOUT_MS_CH,
    )

    logging.info("Created kafka_point.")

    with kafka_point as consumer, connect(settings.CLICKHOUSE_DSN) as conn_ch, conn_ch.cursor() as cursor:
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
