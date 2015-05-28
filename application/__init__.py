from flask import Flask, render_template, request, url_for
from pymongo import MongoClient
from flask.ext.socketio import SocketIO, emit
from bson.objectid import ObjectId

import uuid

client = MongoClient()
db = client.dev_db
app = None
socketio = None

def get_socket():
    global socketio

    if socketio:
        return socketio
    else:
        socketio = SocketIO(get_app())
        @socketio.on('connect')
        def on_connect():
            pass

        return socketio

def get_app():
    if app:
        return app
    else:
        return create_app()

def create_app():
    global app
    app = Flask(__name__, static_url_path='')

    def register_module(blueprint, controller):
        controller.register(blueprint)
        app.register_blueprint(blueprint)

    from controllers.PlayerApiController import blueprint as player_api_module, PlayerApiController as player_api_controller
    from controllers.MatchApiController import blueprint as match_api_module, MatchApiController as match_api_controller
    from controllers.TournamentApiController import blueprint as tournament_api_module, TournamentApiController as tournament_api_controller
    import controllers.MainViewController

    register_module(player_api_module, player_api_controller)
    register_module(match_api_module, match_api_controller)
    register_module(tournament_api_module, tournament_api_controller)

    return app

