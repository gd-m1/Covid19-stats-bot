import os
from datetime import datetime

from pymongo import MongoClient


db = MongoClient(os.getenv('MONGO_LINK'))[os.getenv('MONGO_DB')]


def save_user_query(db, country, effective_user):
    db.country_stats.insert_one({
        'date': datetime.now(),
        'country': country.lower(),
        'username': effective_user.first_name
    })


def get_users_queries(db):
    queries = db.country_stats.aggregate([
        {'$group': {'_id': '$country', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ])
    users = db.country_stats.aggregate([
        {'$group': {'_id': '$username', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ])
    return {'queries': list(queries), 'users': list(users)}
