from flask import request, Blueprint
from flask.views import MethodView

from application.controllers.ApiController import ApiController

from application.daos.TournamentDao import TournamentDao
from application.models.Tournament import Tournament

blueprint = Blueprint('tournament_api', __name__, url_prefix='/api/tournaments')


class TournamentApiController(ApiController):

    url_rules = {
        'index': ['/', ('GET','POST',), {'tournament_id': None}],
        'select': ['/<tournament_id>', ('GET','PUT','DELETE',)],
        'games': ['/<uid>/games', ('GET',)],
        'participants': ['/<uid>/participants', ('GET',)]
    }

    def get(self, tournament_id):
        if tournament_id:
            if self.get_endpoint() == 'games':
                return self.getTournamentGames(uid)

            elif self.get_endpoint() == 'participants':
                return self.getTournamentPlayers(uid)

            else:
                query = TournamentDao().retrieveById(tournament_id)
                return self.gen_response(query)
        else:
            query = TournamentDao().retrieveAll()
            return self.gen_response(query)

    def post(self):
        tournament = Tournament(
                TournamentDao().getValidId(),
                request.json['name'],
                request.json['players'],
                request.json['format'],
                request.json['games'])

        query = TournamentDao().create(tournament)
        return self.gen_response(query)


    def put(self, tournament_id):
        tournament = Tournament(
                tournament_id,
                request.json['name'],
                request.json['players'],
                request.json['format'],
                request.json['games'])

        query = TournamentDao().updateById(tournament_id, tournament)
        return self.gen_response(query)

    def delete(self, tournament_id):
        query = TournamentDao().destroyById(tournament_id)
        return self.gen_response(query)

    def getTournamentPlayers(tournament_id):
        #TODO
        return

    def getTournamentGames(tournament_id):
        #TODO
        return
