from flask import json

from application.daos.Utility import get_database, generate_response
from application.models.Player import Player

class PlayerDao:

    global players 
    players = get_database().players

    def create(self, request):
        new_player = Player(request.json['id'], request.json['name'])
        return generate_response(players.insert(new_player))

    def retrieveAll(self):
        return generate_response(players.find())
    
    def retrieveById(self, id):
        return generate_response(players.find_one({'_id': id}))

    def retrieveByName(self, name):
        return generate_response(players.find_one({'name': name}))
    
    def updateById(self, id, request):
        #TODO
        return generate_response(players.update({'_id': id}, request))

    def updateByName(self, name, request):
        #TODO
        return generate_response(players.update({'name': name}, request))

    def destroyById(self, id):
        return generate_response(players.remove({'_id': id}))

    def destroyByName(self, name):
        return generate_response(players.remove({'name': name}))


