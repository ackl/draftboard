from pymongo import MongoClient

from application.models.Tournament import Tournament

class TournamentDao:

    global tournaments
    tournaments = MongoClient().dev_db.tournaments

    def create(self, tournament):
        return tournaments.insert(tournament.__dict__)

    def retrieveAll(self):
        return tournaments.find()

    def retrieveById(self, id):
        return tournaments.find_one({'id': int(id)})

    def retrieveByName(self, name):
        return tournaments.find_one({'name': name})

    def updateById(self, id, request):
        return tournaments.update({'id': int(id)}, request)

    def updateByName(self, name, request):
        return tournaments.update({'name': name}, request)

    def destroyById(self, id):
        return tournaments.remove({'id': int(id)})

    def destroyByName(self, name):
        return tournaments.remove({'name': name})
    

    def getValidId(self):
        max = 0
        for tournament in tournaments.find():
            try:
                if tournament['id'] > max:
                    max = tournament['id']
            except:
                pass

        return max + 1


