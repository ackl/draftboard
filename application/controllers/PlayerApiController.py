from application import app

from application.daos.PlayerDao import PlayerDao
from application.daos.GameDao import GameDao
from application.daos.TournamentDao import TournamentDao 

class PlayerApiController:

    url = '/api/players'

    @app.route(url + '/')
    def getPlayers():
        return PlayerDao().retrieveAll()

    @app.route(url + '/', methods=['POST'])
    def postPlayer():
        PlayerDao().create(request)

    @app.route(url + '/<player_name>')
    def getPlayer(player_name):
        return PlayerDao().retrieveByName(player_name)

    @app.route(url + '/<player_name>', methods=['PUT'])
    def putPlayer(player_name):
        PlayerDao().updateByName(request)

    @app.route(url + '/<player_name>', methods=['DELETE'])
    def deletePlayer(player_name):
        PlayerDao().destroyByName(player_name)

    @app.route(url + '/<player_name>/games')
    def getPlayerGames(player_name):
        #TODO
        return GameDao().retrieveByPlayerName(player_name)

    @app.route(url + '/<player_name>/tournaments')
    def getPlayerTournaments(player_name):
        #TODO
        return TournamentDao().retrieveByPlayerName(player_name)
        
