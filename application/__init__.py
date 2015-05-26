from flask import Flask


def create_app():

    app = Flask(__name__, static_url_path='')

    def register_module(blueprint, controller):
        controller.register(blueprint)
        app.register_blueprint(blueprint)

    from controllers.PlayerApiController import blueprint as player_api_module, PlayerApiController as player_api_controller
    register_module(player_api_module, player_api_controller)

    return app
