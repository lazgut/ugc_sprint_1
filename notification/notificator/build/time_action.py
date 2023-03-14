import logging
import os
from logging import getLogger
from typing import Iterable

import psycopg
from psycopg.rows import dict_row

from .senders.email import EmailSender

logger = getLogger()
logging.basicConfig(level=logging.INFO)


connection = psycopg.connect(
    host=os.environ["PG_HOST"],
    port=os.environ["PG_PORT"],
    user=os.environ["PG_USER"],
    password=os.environ["PG_PASSWORD"],
    dbname=os.environ["PG_DB_NAME"],
    row_factory=dict_row
)


def on_time():
    if True:
        # Place check here, is we really need to send something
        # We need to scan notification_patterns, read condition there
        # then scan our UGC database and check for condition is True.
        logger.info("Invoked on time")
        users = get_all_users()
        for user in users:
            destination = [user["email"]]  # , "kaysaki@yandex.ru"]
            subject = "Привет!"
            html_template = 'mail.html'
            title = 'Новое письмо!'
            text = 'Произошло что-то интересное! :)'
            image = 'https://upload.wikimedia.org/wikipedia/ru/4/4d/Wojak.png'

            EmailSender.send_mail(destination, subject, html_template, title, text, image)
            logger.info(f"Sent to {destination}")
            print(f"Sent to {destination}")


# TODO Make async?
def get_all_users() -> Iterable[dict]:
    sql = "SELECT * FROM auth.users"
    cur = connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        yield item
