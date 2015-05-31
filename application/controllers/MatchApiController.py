from flask import request, Blueprint
from flask.views import MethodView

from application.controllers.ApiController import ApiController

from application.daos.MatchDao import MatchDao
from application.models.Match import Match
from application.errors import NoSuchFieldError, MissingRequiredFieldError, TypeCoercionError, InvalidFieldValueError

blueprint = Blueprint('match_api', __name__, url_prefix='/api/matches')


class MatchApiController(ApiController):
    url_rules = {
        'index': ['/', ('GET',), {'match_id': None}],
        'add': ['/', ('POST',)],
        'select': ['/<match_id>', ('GET','PUT','DELETE',)]
    }

    def get(self, match_id):
        if match_id:
            return self.gen_response(Match.query({'_id': match_id}))
        else:
            query = Match.query()
            return self.gen_response(query)

    def post(self):
        try:
            match = Match.create(request.json)
            return self.gen_response(match)

        except (NoSuchFieldError, TypeCoercionError, MissingRequiredFieldError, InvalidFieldValueError) as e:
            return self.error_response(e)


    def put(self, match_id):
        match = Match.query({'_id': match_id})

        try:
            match.update(request.json)
        except Exception as e:
            return self.error_response(e)

        return self.gen_response(match)

    def delete(self, match_id):
        query = Match.destroy({'_id': match_id})
        return self.gen_response(query)
