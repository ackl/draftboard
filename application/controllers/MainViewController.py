from flask import Flask, render_template, request, url_for, Blueprint
from flask.views import MethodView
from flask.ext.socketio import SocketIO, emit
from bson.objectid import ObjectId

import uuid

from application.controllers.ApiController import ApiController
from application.daos.PlayerDao import PlayerDao

#from application.daos.GameDao import GameDao
#from application.models.Game import Game

blueprint = Blueprint('main_view', __name__, url_prefix='/')


class MainViewController(ApiController):
    url_rules = {
        'index': ['/', ('GET','POST',)]
    }

    playerDao = PlayerDao()

    def get(self):
        player_list = []

        for pl in self.playerDao.retrieveAll():
            player_list.append(pl)

        return render_template("index.html", players=player_list)
