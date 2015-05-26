from flask import request

from application import app
from application.Utility import gen_response
from application.daos.GameDao import GameDao
from application.models.Game import Game

class GameApiController:

    url = '/api/games'

    @app.route(url + '/')
    def getGames():
        query = GameDao().retrieveAll()
        return gen_response(query)

    @app.route(url + '/', methods=['POST'])
    def postGame():
        game = Game(
                GameDao().getValidId(),
                request.json['players'],
                request.json['format'])

        query = GameDao().create(game)
        return gen_response(query)

    @app.route(url + '/<game_id>')
    def getGame(game_id):
        query = GameDao().retrieveById(game_id)
        return gen_response(query)

    @app.route(url + '/<game_id>', methods=['PUT'])
    def putGame(game_id):
        game = Game(
                game_id,
                request.json['players'],
                request.json['format'])

        query = GameDao().updateById(game_id, game)
        return gen_response(query)

    @app.route(url + '/<game_id>', methods=['DELETE'])
    def deleteGame(game_id):
        query = GameDao().destroyById(game_id)
        return gen_response(query)
