from flask import json

from application.daos.Utility import get_database, generate_response
from application.models.Game import Game

class GameDao:

    global games
    games = get_database().games

    def create(self, request):
        new_game = Game() #TODO: serialize json request to Game object
        return generate_response(games.insert(new_game))

    def retrieveAll(self):
        return generate_response(games.find())

    def retrieveById(self, id):
        return generate_response(games.find_one({'_id': id}))

    def updateById(self, id, request):
        #TODO
        return generate_response(games.find_one_and_update({'_id': id}, request))

    def deleteById(self, id):
        return generate_response(games.find_one_and_delete({'_id': id}))
