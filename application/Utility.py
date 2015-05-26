from flask import Response, make_response
from bson.json_util import dumps

def gen_response(query):
    response = Response(dumps(query), mimetype='application/json')
    return make_response(response)

