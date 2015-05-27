from flask import request, Blueprint
from flask.views import MethodView

from application.controllers.ApiController import ApiController

from application.daos.GameDao import GameDao
from application.models.Game import Game

blueprint = Blueprint('game_api', __name__, url_prefix='/api/games')


class GameApiController(ApiController):
    url_rules = {
        'index': ['/', ('GET',), {'game_id': None}],
        'add': ['/', ('POST',)],
        'select': ['/<game_id>', ('GET','PUT','DELETE',)]
    }

    def get(self, game_id):
        if game_id:
            query = GameDao().retrieveById(game_id)
            return self.gen_response(query)
        else:
            query = GameDao().retrieveAll()
            return self.gen_response(query)

    def post(self):
        game = Game(
                GameDao().getValidId(),
                request.json['players'],
                request.json['format'])

        query = GameDao().create(game)
        return self.gen_response(query)

    def put(self, game_id):
        game = Game(
                game_id,
                request.json['players'],
                request.json['format'])

        query = GameDao().updateById(game_id, game)
        return self.gen_response(query)

    def delete(self, game_id):
        query = GameDao().destroyById(game_id)
        return self.gen_response(query)
