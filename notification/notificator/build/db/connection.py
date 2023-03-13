
import psycopg
from psycopg.rows import dict_row

from build.config import settings


connection = psycopg.connect(host=settings.postgres_host,
                             port=settings.postgres_port,
                             user=settings.postgres_user,
                             password=settings.postgres_password,
                             dbname="notification",
                             row_factory=dict_row)

