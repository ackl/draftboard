from flask import Flask, render_template, request, url_for
from pymongo import MongoClient
from flask.ext.socketio import SocketIO, emit


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
        return '200'
    else:
        return 'invalid syntax'


@socketio.on('lose_life', namespace='/life')
def decreaseLife(data):
    player = changeLife(False, data['amount'], data['player'])
    emit('response', {'name': player['name'], 'life': player['life']}, broadcast=True)

@socketio.on('gain_life', namespace='/life')
def increaseLife(data):
    player = changeLife(True, data['amount'], data['player'])
    emit('response', {'name': player['name'], 'life': player['life']}, broadcast=True)


def getPlayerByName(name):
    return players.find_one({'name': name});

def changeLife(increment, amount, name):
    player = getPlayerByName(name)
    life = player['life']

    if increment:
        life += amount
    else:
        life -= amount

    players.update({'_id': player['_id']}, {"$set": {"life": life}}, upsert=False)
    return getPlayerByName(name)



if __name__ == "__main__":
    app.debug = True
    #app.run()
    socketio.run(app, host='0.0.0.0')


