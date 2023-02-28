import datetime
import random

import pymongo
MONGODB_URI = 'mongodb://localhost:27017'
client = pymongo.MongoClient(MONGODB_URI)
db = client['test']
likes = db.get_collection('likes')

users_file = '../../users'
movies_file = '../../movies'
with open(users_file) as fu:
    users = [s.strip() for s in fu.readlines()]
with open(movies_file) as fm:
    movies = [s.strip() for s in fm.readlines()]

ts = datetime.datetime.now()
for million in range(1):
    print("million", million)
    for i_batch in range(1000):
        batch = []
        for i_document in range(1000):
            user = random.choice(users)
            movie = random.choice(movies)
            batch.append({'user': user, 'movie': movie,
                          'timestamp': datetime.datetime.now()})
        likes.insert_many(batch)
td = datetime.datetime.now() - ts
print('time', td) # 1m - 2:14 min.