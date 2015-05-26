from flask import request

from application import app
from application.Utility import gen_response
from application.daos.TournamentDao import TournamentDao
from application.models.Tournament import Tournament

class TournamentApiController:

    url = '/api/tournaments'

    @app.route('/')
    def getTournaments():
        query = TournamentDao().retrieveAll()
        return gen_response(query)

    @app.route('/', methods=['POST'])
    def postTournament():
        tournament = Tournament(
                TournamentDao().getValidId(),
                request.json['name'],
                request.json['players'],
                request.json['format'],
                request.json['games'])

        query = TournamentDao().create(tournament)
        return gen_response(query)

    @app.route('/<tournament_id>')
    def getTournament(tournament_id):
        query = TournamentDao().retrieveById(tournament_id)
        return gen_response(query)

    @app.route('/<tournament_id>', methods=['PUT'])
    def putTournament(tournament_id):
        tournament = Tournament(
                tournament_id,
                request.json['name'],
                request.json['players'],
                request.json['format'],
                request.json['games'])

        query = TournamentDao().updateById(tournament_id, tournament)
        return gen_response(query)

    @app.route('/<tournament_id>', methods=['DELETE'])
    def deleteTournament(tournament_id):
        query = TournamentDao().destroyById(tournament_id)
        return gen_response(query)

    @app.route('/<tournament_id>/participants')
    def getTournamentPlayers(tournament_id):
        #TODO
        return 

    @app.route('/<tournament_id>/games')
    def getTournamentGames(tournament_id):
        #TODO
        return
