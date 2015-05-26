from flask import Flask


def create_app():

    app = Flask(__name__, static_url_path='')

    def register_module(blueprint, controller):
        controller.register(blueprint)
        app.register_blueprint(blueprint)

    from controllers.PlayerApiController import blueprint as player_api_module, PlayerApiController as player_api_controller
    from controllers.GameApiController import blueprint as game_api_module, GameApiController as game_api_controller
    from controllers.TournamentApiController import blueprint as tournament_api_module, TournamentApiController as tournament_api_controller

    register_module(player_api_module, player_api_controller)
    register_module(game_api_module, game_api_controller)
    register_module(tournament_api_module, tournament_api_controller)

    return app
