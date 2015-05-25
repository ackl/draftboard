from flask import Flask, render_template, request, url_for
from pymongo import MongoClient
from flask.ext.socketio import SocketIO, emit
from bson.objectid import ObjectId

import uuid

# Setup
app = Flask(__name__)
socketio = SocketIO(app)
client = MongoClient()

db = client.dev_db
players = db.players


# Render index view
@app.route("/")
def index():
    player_list = []

    for pl in players.find():
        player_list.append(pl)

    return render_template("index.html", players=player_list)


# Create a new player
@app.route('/newplayer', methods = ['POST'])
def newPlayer():
    if 'name' in request.json:
        print request.json['name']

        player = {
                "name": request.json['name'],
                "life": 20,
                "games": []
                }

        player_id = players.insert(player)
        socketio.emit('testing', {'message': 'hi'}, broadcast=True)

        #socketio.emit('new_player',
                #{'player_id': player_id, 'life': player['life'], 'name': player['name']},
                      #namespace='/life', broadcast=True)

        #emit('new_player', {'player_id': player_id, 'life': player['life'], 'name': player['name']}, broadcast=True, namespace='/life')
        return '200'
    else:
        return 'invalid syntax'


@socketio.on('lose_life', namespace='/draftboard')
def decreaseLife(data):
    player = changeLife(False, data['amount'], data['player_id'])
    emit('response', {'player_id': str(player['_id']), 'life': player['life']}, broadcast=True)

@socketio.on('gain_life', namespace='/draftboard')
def increaseLife(data):
    player = changeLife(True, data['amount'], data['player_id'])
    emit('response', {'player_id': str(player['_id']), 'life': player['life']}, broadcast=True)

@socketio.on('create_player', namespace='/draftboard')
def createPlayer(data):
    player = {
            "name": data['name'],
            "life": 20,
            "games": []
            }

    player_id = players.insert(player)

    emit('new_player', {'player': {'name': player['name'], 'life': player['life'], 'games': player['games'], '_id': str(player_id)}}, broadcast=True)

def getPlayerByName(name):
    return players.find_one({'name': name});

def getPlayerById(_id):
    _id = ObjectId(_id)
    return players.find_one({'_id': _id});

def changeLife(increment, amount, _id):
    player = getPlayerById(_id)
    life = player['life']

    if increment:
        life += amount
    else:
        life -= amount

    players.update({'_id': player['_id']}, {"$set": {"life": life}}, upsert=False)
    return getPlayerById(_id)



if __name__ == "__main__":
    app.debug = True
    socketio.run(app, host='0.0.0.0')


