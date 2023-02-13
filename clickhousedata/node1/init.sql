CREATE DATABASE shard;
CREATE DATABASE replica;
CREATE TABLE shard.cinema_ch (id String, event_time String, topic String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/cinema_ch', 'replica_1') PARTITION BY toString(topic) ORDER BY id;
CREATE TABLE replica.cinema_ch (id String, event_time String, topic String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/cinema_ch', 'replica_2') PARTITION BY toString(topic) ORDER BY id;
CREATE TABLE default.cinema_ch (id String, event_time String, topic String) ENGINE = Distributed('company_cluster', '', cinema_ch, rand());