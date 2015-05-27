from flask import request, Blueprint
from flask.views import MethodView

from application.controllers.ApiController import ApiController

from application.daos.PlayerDao import PlayerDao
from application.daos.GameDao import GameDao
from application.models.Player import Player
from application import get_socket
from flask.ext.socketio import emit

blueprint = Blueprint('player_api', __name__, url_prefix='/api/players')

socketio = get_socket()
playerDao = PlayerDao()

def changeLife(increment, amount, _id):
    player = playerDao.retrieveById(_id)

    if increment:
        player.life += amount
    else:
        player.life -= amount

    playerDao.updateById(_id, player)

    player = playerDao.retrieveById(_id)
    return player


@socketio.on('lose_life')
def decreaseLife(data):
    player = changeLife(False, data['amount'], data['player_id'])
    emit('response', {'player_id': str(player.id), 'life': player.life}, broadcast=True)

@socketio.on('gain_life')
def increaseLife(data):
    player = changeLife(True, data['amount'], data['player_id'])
    emit('response', {'player_id': str(player.id), 'life': player.life}, broadcast=True)

@socketio.on('broadcast_message:send')
def broadcastMessage(data):
    emit('broadcast_message:receive', {'message': data['message']}, broadcast=True)

class PlayerApiController(ApiController):

    url_rules = {
        'index': ['/', ('GET',), {'uid': None}],
        'create': ['/', ('POST',)],
        'select': ['/<uid>', ('GET','PUT','DELETE',)],
        'games': ['/<uid>/games', ('GET',)],
        'tournaments': ['/<uid>/tournaments', ('GET',)]
    }

    def get(self, uid):
        if uid:
            if self.get_endpoint() == 'games':
                return self.get_games(uid)

            elif self.get_endpoint() == 'tournaments':
                return self.get_tournaments(uid)

            else:
                query = PlayerDao().retrieveById(uid)
                return self.gen_response(query)

        else:
            query = PlayerDao().retrieveAll()
            return self.gen_response(query)

    def post(self):
        player = PlayerDao().create(request.json['name'])

        socketio.emit('new_player', {'player': {'name': player.name, 'life': player.life, '_id': str(player.id)}})
        return '200'


    def put(self, uid):
        player = Player(uid, request.json['name'])
        player.life = request.json['life']

        query = PlayerDao().updateById(uid, player)
        return self.gen_response(query)

    def delete(self, uid):
        query = PlayerDao().destroyById(uid)
        return self.gen_response(query)


    def get_games(self, uid):
        player = PlayerDao().retrieveById(uid)
        games = []
        for game in GameDao().retrieveAll():
            if str(player['_id']) in game['players']:
                games.append(game)

        return self.gen_response(games)

    def getTournaments(self, uid):
        #TODO
        return '200'

#PlayerApiController.register(blueprint)
