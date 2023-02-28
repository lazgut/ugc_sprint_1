import datetime
import random

import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='app', password='123qwe', database='test')

users_file = '../../users'
movies_file = '../../movies'
with open(users_file) as fu:
    users = [s.strip() for s in fu.readlines()]
with open(movies_file) as fm:
    movies = [s.strip() for s in fm.readlines()]


cur = conn.cursor()
sql = "INSERT INTO public.likes (\"user\", movie, timestamp) VALUES (%s, %s, %s)" \
      " ON CONFLICT (\"user\", movie) DO UPDATE SET" \
      "\"user\"=excluded.user," \
      "movie=excluded.movie," \
      "timestamp=excluded.timestamp"
for million in range(28):
    ts = datetime.datetime.now()
    for i_batch in range(1000):
        print('\tbatch', i_batch)
        batch = []
        for i_document in range(1000):
            user = random.choice(users)
            movie = random.choice(movies)
            batch.append((user, movie, datetime.datetime.now()))
        try:
            cur.execute('START TRANSACTION')
            cur.executemany(sql, batch)
        except psycopg2.errors.UniqueViolation:
            cur.execute("ROLLBACK")
            print('rollback')
    td = datetime.datetime.now() - ts
    print('million', million, '\ttime', td) # 1m - 2:04, 2:19 min.
    # 11- 1:13 hour.