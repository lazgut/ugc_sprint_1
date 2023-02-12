# Краткое описание работы с ETL

Для работы ETL необходимо создать реплицированную шардированную таблицу на нескольких нодах.

Подключаемся к первому шарду:
- `docker exec -it clickhouse-node1 clickhouse-client`

Вводим последовательно следующие команды:
- `CREATE DATABASE shard;`
- `CREATE DATABASE replica;`
- `CREATE TABLE shard.cinema_ch (id String, event_time String, topic String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/cinema_ch', 'replica_1') PARTITION BY toString(topic) ORDER BY id;`
- `CREATE TABLE replica.cinema_ch (id String, event_time String, topic String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/cinema_ch', 'replica_2') PARTITION BY toString(topic) ORDER BY id;`
- `CREATE TABLE default.cinema_ch (id String, event_time String, topic String) ENGINE = Distributed('company_cluster', '', cinema_ch, rand());`

Подключаемся ко второму шарду:
- `docker exec -it clickhouse-node3 clickhouse-client`

Также последовательно вводим команды:
- `CREATE DATABASE shard;`
- `CREATE DATABASE replica;`
- `CREATE TABLE shard.cinema_ch (id String, event_time String, topic String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/cinema_ch', 'replica_1') PARTITION BY toString(topic) ORDER BY id;`
- `CREATE TABLE replica.cinema_ch (id String, event_time String, topic String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/cinema_ch', 'replica_2') PARTITION BY toString(topic) ORDER BY id;`
- `CREATE TABLE default.cinema_ch (id String, event_time String, topic String) ENGINE = Distributed('company_cluster', '', cinema_ch, rand());`

Теперь ETL будет корректно загружать данные из Kafka в Clickhouse