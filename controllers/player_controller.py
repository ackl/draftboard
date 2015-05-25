from dao.* import *

class PlayerApiController:

    url = '/api/players'

    def __init__(self):
        self.player_dao = PlayerDao()
        self.game_dao = GameDao()
        self.tournament_dao = TournamentDao()

    @app.route(url + '/')
    def getPlayers():
        return player_dao.retrieveAll()

    @app.route(url + '/', methods=['POST'])
    def postPlayer():
        player_dao.create(request)

    @app.route(url + '/<player_name>')
    def getPlayer(player_name):
        return player_dao.retrieveByName(player_name)

    @app.route(url + '/<player_name>', methods=['PUT'])
    def putPlayer(player_name):
        player_dao.updateByName(request)

    @app.route(url + '/<player_name>', methods=['DELETE'])
    def deletePlayer(player_name):
        player_dao.destroyByName(player_name)

    @app.route(url + '/<player_name>/games')
    def getPlayerGames(player_name):
        return game_dao.retrieveByPlayerName(player_name)

    @app.route(url + '/<player_name>/tournaments')
    def getPlayerTournaments(player_name):
        return tournament_dao.retrieveByPlayerName(player_name)
        
