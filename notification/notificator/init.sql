create table if not exists notification_pattern
(
    id           serial primary key
    type_         smallint     not null,
    pattern_file varchar(100) not null,
    actual_time  integer,
    settings     json,

);

comment on column notification_pattern.type is 'by event / by time / manual';

comment on column notification_pattern.pattern_file is 'A path to the pattern file';

comment on column notification_pattern.actual_time is 'in seconds';

alter table notification_pattern
    owner to app;

create table if not exists types
(
    id   serial primary key,
    name varchar  not null
);

alter table types
    owner to app;

create table if not exists notification_event
(
    pattern    integer not null
        constraint notification_event_notification_pattern_null_fk
            references notification_pattern,
    source     json,
    start_time time    not null,
    end_time   time
);

comment on column notification_event.pattern is 'Link to notification_pattern';

comment on column notification_event.source is 'A reason to launch';

alter table notification_event
    owner to app;

INSERT INTO types (name) VALUES ('by event');
INSERT INTO types (name) VALUES ('by time');
INSERT INTO types (name) VALUES ('manual');