from application import app

from application.daos.GameDao import GameDao

class GameApiController:

    url = '/api/games'

    @app.route(url + '/')
    def getGames():
        return GameDao().retrieveAll()

    @app.route(url + '/', methods=['POST'])
    def postGame():
        GameDao().create(request)

    @app.route(url + '/<game_id>')
    def getGame(game_id):
        return GameDao().retrieveById(game_id)

    @app.route(url + '/<game_id>', methods=['PUT'])
    def putGame(game_id):
        GameDao().updateById(game_id, request)

    @app.route(url + '/<game_id>', methods=['DELETE'])
    def deleteGame(game_id):
        GameDao().destroyById(game_id)
