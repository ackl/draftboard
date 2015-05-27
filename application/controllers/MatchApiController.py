from flask import request, Blueprint
from flask.views import MethodView

from application.controllers.ApiController import ApiController

from application.daos.MatchDao import MatchDao
from application.models.Match import Match

blueprint = Blueprint('match_api', __name__, url_prefix='/api/matches')


class MatchApiController(ApiController):
    url_rules = {
        'index': ['/', ('GET',), {'match_id': None}],
        'add': ['/', ('POST',)],
        'select': ['/<match_id>', ('GET','PUT','DELETE',)]
    }

    def get(self, match_id):
        if match_id:
            query = MatchDao().retrieveById(match_id)
            return self.gen_response(query)
        else:
            query = MatchDao().retrieveAll()
            return self.gen_response(query)

    def post(self):
        match = Match(
                MatchDao().getValidId(),
                request.json['player_scores'],
                request.json['format'])

        query = MatchDao().create(match)
        return self.gen_response(query)

    def put(self, match_id):
        match = Match(
                match_id,
                request.json['player_scores'],
                request.json['format'])

        query = MatchDao().updateById(match_id, match)
        return self.gen_response(query)

    def delete(self, match_id):
        query = MatchDao().destroyById(match_id)
        return self.gen_response(query)
