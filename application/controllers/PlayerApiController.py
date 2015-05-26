from flask import request, Blueprint
from flask.views import MethodView

from application.controllers.ApiController import ApiController

from application.daos.PlayerDao import PlayerDao
from application.models.Player import Player

blueprint = Blueprint('player_api', __name__, url_prefix='/api/players')

class PlayerApiController(ApiController):

    url_rules = {
        'index': ['/', ('GET','POST',), {'uid': None}],
        'select': ['/<uid>', ('GET','PUT','DELETE',)],
        'games': ['/<uid>/games', ('GET',)],
        'tournaments': ['/<uid>/tournaments', ('GET',)]
    }

    def get(self, uid):
        if uid:
            if self.get_endpoint() == 'games':
                return self.getGames(uid)

            elif self.get_endpoint() == 'tournaments':
                return self.getTournaments(uid)

            else:
                query = PlayerDao().retrieveById(uid)
                return self.gen_response(query)

        else:
            query = PlayerDao().retrieveAll()
            return self.gen_response(query)

    def post(self):
        player = Player(
                PlayerDao().getValidId(),
                request.json['name'])

        query = PlayerDao().create(player)
        return self.gen_response(query)


    def put(self, uid):
        player = Player(uid, request.json['name'])
        player.life = request.json['life']

        query = PlayerDao().updateById(uid, player)
        return self.gen_response(query)

    def delete(self, uid):
        query = PlayerDao().destroyById(uid)
        return self.gen_response(query)

    def getGames(self, uid):
        #TODO
        return '200'

    def getTournaments(self, uid):
        #TODO
        return '200'

#PlayerApiController.register(blueprint)
