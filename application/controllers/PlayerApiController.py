from flask import request

from application import app
from application.Utility import gen_response
from application.daos.PlayerDao import PlayerDao
from application.models.Player import Player

class PlayerApiController:

    url = '/api/players'

    @app.route(url + '/')
    def getPlayers():
        query = PlayerDao().retrieveAll()
        return gen_response(query)

    @app.route(url + '/', methods=['POST'])
    def postPlayer():
        player = Player(
                PlayerDao().getValidId(), 
                request.json['name'])

        query = PlayerDao().create(player)
        return gen_response(query)

    @app.route(url + '/<player_id>')
    def getPlayer(player_id):
        query = PlayerDao().retrieveById(player_id)
        return gen_response(query)

    @app.route(url + '/<player_id>', methods=['PUT'])
    def putPlayer(player_id):
        player = Player(
                player_id,
                request.json['name'])
        player.life = request.json['life']

        query = PlayerDao().updateById(player_id, player)
        return gen_response(query)

    @app.route(url + '/<player_id>', methods=['DELETE'])
    def deletePlayer(player_id):
        query = PlayerDao().destroyById(player_id)
        return gen_response(query)

    @app.route(url + '/<player_name>/games')
    def getPlayerGames(player_name):
        #TODO
        return

    @app.route(url + '/<player_name>/tournaments')
    def getPlayerTournaments(player_name):
        #TODO
        return 
        
