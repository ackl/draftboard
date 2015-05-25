from dao.* import *

class GameiApiController:

    url = '/api/games'

    player_dao = PlayerDao()
    game_dao = GameDao()

    def __init__(self):

    @app.route('/')
    def getGames():
        return game_dao.retrieveAll()

    @app.route('/', methods=['POST'])
    def postGame():
        game_dao.createGame(request)

    @app.route('/<game_id>')
    def getGame(game_id):
        return game_dao.retrieveById(game_id)

    @app.route('/<game_id>', methods=['PUT'])
    def putGame(game_id):
        game_dao.updateById(game_id, request)

    @app.route('/<game_id>', methods=['DELETE'])
    def deleteGame(game_id):
        game_dao.destroyById(game_id)

