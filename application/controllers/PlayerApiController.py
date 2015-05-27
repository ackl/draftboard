from flask import request, Blueprint, jsonify
from flask.views import MethodView

from application.controllers.ApiController import ApiController

from application.daos.PlayerDao import PlayerDao
from application.daos.MatchDao import MatchDao
from application.daos.TournamentDao import TournamentDao
from application.models.Player import Player
from application import get_socket
from flask.ext.socketio import emit
from pymongo.errors import InvalidId

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
        'matches': ['/<uid>/matches', ('GET',)],
        'tournaments': ['/<uid>/tournaments', ('GET',)]
    }

    def get(self, uid):
        if uid:
            try:
                player = PlayerDao().retrieveById(uid)
            except InvalidId as e:
                return jsonify({
                    'error_type': type(e).__name__,
                    'error_message': e.args[0]
                })

            if self.get_endpoint() == 'matches':
                return self.gen_response(player.get_matches(MatchDao().retrieveAll()))

            elif self.get_endpoint() == 'tournaments':
                return self.gen_response(player.get_tournaments(TournamentDao().retrieveAll()))

            else:
                query = PlayerDao().retrieveById(uid)
                return self.gen_response(query)

        else:
            query = PlayerDao().retrieveAll()
            return self.gen_response(query)
            #return query

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


    def get_matches(self, uid):
        player = PlayerDao().retrieveById(uid)
        matches = []
        for match in MatchDao().retrieveAll():
            if str(player['_id']) in match['player_scores']:
                matches.append(match)

        return self.gen_response(matches)

    def getTournaments(self, uid):
        #TODO
        return '200'

#PlayerApiController.register(blueprint)
