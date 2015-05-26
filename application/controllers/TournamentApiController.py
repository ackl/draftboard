from application import app

from application.daos.PlayerDao import PlayerDao
from application.daos.GameDao import GameDao
from application.daos.TournamentDao import TournamentDao

class TournamentApiController:

    url = '/api/tournaments'

    @app.route('/')
    def getTournaments():
        return TournamentDao().retrieveAll()

    @app.route('/', methods=['POST'])
    def postTournament():
        TournamentDao().create(request)

    @app.route('/<tournament_id>')
    def getTournament(tournament_id):
        return TournamentDao().retrieveById(tournament_id)

    @app.route('/<tournament_id>', methods=['PUT'])
    def putTournament(tournament_id):
        TournamentDao().updateById(tournament_id, request)

    @app.route('/<tournament_id>', methods=['DELETE'])
    def deleteTournament(tournament_id):
        TournamentDao().destroyById(tournament_id)

    @app.route('/<tournament_id>/participants')
    def getTournamentPlayers(tournament_id):
        #TODO
        return PlayerDao().retrieveByTournamentId(tournament_id)

    @app.route('/<tournament_id>/games')
    def getTournamentGames(tournament_id):
        #TODO
        return GameDao().retrieveByTournamentId(tournament_id)
