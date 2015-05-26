from flask import json

from application.daos.Utility import get_database, generate_response
from application.models.Tournament import Tournament

class TournamentDao:

    global tournaments
    tournaments = get_database().tournaments

    def create(self, request):
        new_tournament = Tournament() #TODO: serialize json request to Tournament object
        return generate_response(tournaments.insert(new_tournament))

    def retrieveAll(self):
        return generate_response(tournaments.find())

    def retrieveById(self, id):
        return generate_response(tournaments.find_one({'_id': id}))

    def retrieveByName(self, name):
        return generate_response(tournaments.find_one({'name': name}))

    def updateById(self, id, request):
        #TODO
        return generate_response(tournaments.find_one_and_update({'_id': id}, request))

    def updateByName(self, name, request):
        #TODO
        return generate_response(tournaments.find_one_and_update({'name': name}, request))

    def deleteById(self, id):
        return generate_response(tournaments.find_one_and_delete({'_id': id}))

    def deleteByName(self, name):
        return generate_response(tournaments.find_one_and_delete({'name': name}))


