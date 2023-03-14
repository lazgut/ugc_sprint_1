import logging
import os
from logging import getLogger
from typing import Iterable

import psycopg
from psycopg.rows import dict_row

from build.common_send import send_all
from build.db.helper import db_helper


logger = getLogger()
logging.basicConfig(level=logging.INFO)


connection_auth = psycopg.connect(
    host=os.environ["PG_HOST"],
    port=os.environ["PG_PORT"],
    user=os.environ["PG_USER"],
    password=os.environ["PG_PASSWORD"],
    dbname=os.environ["PG_DB_NAME"],
    row_factory=dict_row
)

connection_notif = psycopg.connect(
    host=os.environ["NOTIFICATION_PG_HOST"],
    port=os.environ["NOTIFICATION_PG_PORT"],
    user=os.environ["NOTIFICATION_PG_USER"],
    password=os.environ["NOTIFICATION_PG_PASSWORD"],
    dbname="notification",
    row_factory=dict_row
)



def on_time():
    if True:
        # Place check here, is we really need to send something
        # We need to scan notification_patterns, read condition there
        # then scan our UGC database and check for condition is True.
        logger.info("Invoked on time")
        users = get_all_users()
        patterns = db_helper.get_time_patterns()
        send_all(users, patterns)


# TODO Make async?
def get_all_users() -> Iterable[dict]:
    sql = "SELECT * FROM auth.users"
    cur = connection_auth.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        yield item
