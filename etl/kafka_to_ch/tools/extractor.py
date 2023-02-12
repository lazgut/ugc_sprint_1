from kafka import KafkaConsumer


class KafkaExtractor:
    def __init__(self, topic: str,
                 auto_offset_reset: str,
                 bootstrap_servers: str, enable_auto_commit: bool,
                 group_id: str,
                 chunk_size=10000,
                 consumer_timeout_ms=1000):
        self.consumer = None
        self.topic = topic
        self.auto_offset_reset = auto_offset_reset
        self.bootstrap_servers = bootstrap_servers
        self.enable_auto_commit = enable_auto_commit
        self.group_id = group_id
        self.consumer_timeout_ms = consumer_timeout_ms
        self.chunk_size = chunk_size
        self.data_extract = []

    def __enter__(self):
        self.consumer = KafkaConsumer(self.topic,
                                      auto_offset_reset=self.auto_offset_reset,
                                      bootstrap_servers=[self.bootstrap_servers],
                                      enable_auto_commit=self.enable_auto_commit,
                                      group_id=self.group_id,
                                      consumer_timeout_ms=self.consumer_timeout_ms)
        return self.consumer

    def __exit__(self, exc_type, exc_value, traceback):
        return self.consumer.close()

    def extract_data(self):
        count = 0
        for message in self.consumer:
            cash_data = []
            count += 1
            cash_data.append(message.key)
            cash_data.append(message.value)
            cash_data.append(message.topic)
            self.data_extract.append(cash_data)
            if count >= self.chunk_size:
                yield self.data_extract
                count = 0
                self.data_extract = []
