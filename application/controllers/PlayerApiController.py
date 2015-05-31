from flask import request, Blueprint, jsonify
from flask.views import MethodView

from application.controllers.ApiController import ApiController

from application.daos.MatchDao import MatchDao
from application.daos.TournamentDao import TournamentDao
from application.models.Player import Player
from application.errors import MongoModelError
from application import get_socket
from flask.ext.socketio import emit
from pymongo.errors import InvalidId

blueprint = Blueprint('player_api', __name__, url_prefix='/api/players')
socketio = get_socket()


class PlayerApiController(ApiController):

    url_rules = {
        'index': ['/', ('GET',), {'uid': None}],
        'create': ['/', ('POST',)],
        'select': ['/<uid>', ('GET','PUT','DELETE',)],
        'matches': ['/<uid>/matches', ('GET',)],
        'current_match': ['/<uid>/matches/current', ('GET',)],
        'tournaments': ['/<uid>/tournaments', ('GET',)]
    }

    def get(self, uid):
        if uid:
            try:
                player = Player.query({'_id': uid})
            except InvalidId as e:
                return jsonify({
                    'error_type': type(e).__name__,
                    'error_message': e.args[0]
                })

            if self.get_endpoint() == 'matches':
                return self.gen_response(player.get_matches())

            elif self.get_endpoint() == 'current':
                return self.gen_response(player.get_current_match())

            elif self.get_endpoint() == 'tournaments':
                return self.gen_response(player.get_tournaments(TournamentDao().retrieveAll()))

            else:
                #query = Player.query({'_id': uid})
                return self.gen_response(player)

        else:
            query = Player.query()
            return self.gen_response(query)

    def post(self):
        try:
            player = Player.create(request.json)
            socketio.emit('new_player', {'player': {'name': player.name, 'life': player.life, '_id': str(player._id)}})
            return self.gen_response(player)
        except MongoModelError as e:
            return self.error_response(e)


    def put(self, uid):
        player = Player.query({'_id': uid})

        try:
            player.update(request.json)
        except MongoModelError as e:
            return self.error_response(e)

        socketio.emit('response', {'player_id': str(player._id), 'life': player.life})
        return self.gen_response(player)

    def delete(self, uid):
        query = Player.destroy({'_id': uid})
        return '200'


    def get_matches(self, uid):
        player = Player.query({'_id': uid})
        matches = []
        for match in MatchDao().retrieveAll():
            if str(player['_id']) in match['player_scores']:
                matches.append(match)

        return self.gen_response(matches)

    def getTournaments(self, uid):
        #TODO
        return '200'

    @socketio.on('broadcast_message:send')
    def broadcastMessage(data):
        emit('broadcast_message:receive', {'message': data['message']}, broadcast=True)

    @socketio.on('lose_life')
    def decreaseLife(data):
        player = Player.query({'_id': data['player_id']})
        player.update({'life': player.life - data['amount']})
        emit('response', {'player_id': str(player._id), 'life': player.life}, broadcast=True)

    @socketio.on('gain_life')
    def increaseLife(data):
        player = Player.query({'_id': data['player_id']})
        player.update({'life': player.life + data['amount']})
        emit('response', {'player_id': str(player._id), 'life': player.life}, broadcast=True)



