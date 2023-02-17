ATTACH TABLE cinema_ch
(
    `id` String,
    `event_time` String,
    `topic` String
)
ENGINE = Distributed('company_cluster', '', 'cinema_ch', rand())
