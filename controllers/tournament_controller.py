from dao.* import *

class TournamentApiController:

    url = '/api/tournaments'

    player_dao = PlayerDao()
    game_dao = GameDao()
    tournament_dao = TournamentDao()

    def __init__(self):

    @app.route('/')
    def getTournaments():
        return tournament_dao.retrieveAll()

    @app.route('/', methods=['POST'])
    def postTournament():
        tournament_dao.create(request)

    @app.route('/<tournament_id>')
    def getTournament(tournament_id):
        return tournament_dao.retrieveById(tournament_id)

    @app.route('/<tournament_id>', methods=['PUT'])
    def putTournament(tournament_id):
        tournament_dao.updateById(tournament_id, request)

    @app.route('/<tournament_id>', methods=['DELETE'])
    def deleteTournament(tournament_id):
        tournament_dao.destroyById(tournament_id)

    @app.route('/<tournament_id>/participants')
    def getTournamentPlayers(tournament_id):
        return player_dao.retrieveByTournamentId(tournament_id)

    @app.route('/<tournament_id>/games')
    def getTournamentGames(tournament_id):
        return game_dao.retrieveByTournamentId(tournament_id)
