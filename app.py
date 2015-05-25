from flask import Flask, render_template, request, url_for
from pymongo import MongoClient


# Setup
app = Flask(__name__)
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

if __name__ == "__main__":
    app.debug = True
    app.run()
