ATTACH TABLE cinema_ch
(
    `id` String,
    `event_time` String,
    `topic` String
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/shard1/cinema_ch', 'replica_2')
PARTITION BY toString(topic)
ORDER BY id
SETTINGS index_granularity = 8192
