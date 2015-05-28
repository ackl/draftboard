from flask import Flask, render_template, request, url_for, Blueprint
from flask.views import MethodView
from flask.ext.socketio import SocketIO, emit
from bson.objectid import ObjectId

import uuid

from application.controllers.ApiController import ApiController

blueprint = Blueprint('main_view', __name__, url_prefix='/')


class MainViewController(ApiController):
    url_rules = {
        'index': ['/', ('GET','POST',)]
    }


    def get(self):
        return render_template("index.html")
