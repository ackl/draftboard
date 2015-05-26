from pymongo import MongoClient
from flask import Response, make_response
from bson.json_util import dumps

def get_database():
    client = MongoClient()
    return client.dev_db

def generate_response(query):
    response = Response(dumps(query), mimetype='application/json')
    return make_response(response)

