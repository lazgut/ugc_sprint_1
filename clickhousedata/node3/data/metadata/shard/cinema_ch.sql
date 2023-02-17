ATTACH TABLE cinema_ch
(
    `id` String,
    `event_time` String,
    `topic` String
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/shard2/cinema_ch', 'replica_1')
PARTITION BY toString(topic)
ORDER BY id
SETTINGS index_granularity = 8192
