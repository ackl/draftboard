from pymongo import MongoClient

from application.models.Tournament import Tournament

class TournamentDao:

    tournaments = MongoClient().dev_db.tournaments

    def create(self, tournament):
        return self.tournaments.insert(tournament.__dict__)

    def retrieveAll(self):
        return self.tournaments.find()

    def retrieveById(self, id):
        return self.tournaments.find_one({'id': int(id)})

    def retrieveByName(self, name):
        return self.tournaments.find_one({'name': name})

    def updateById(self, id, request):
        return self.tournaments.update({'id': int(id)}, request)

    def updateByName(self, name, request):
        return self.tournaments.update({'name': name}, request)

    def destroyById(self, id):
        return self.tournaments.remove({'id': int(id)})

    def destroyByName(self, name):
        return self.tournaments.remove({'name': name})


    def getValidId(self):
        max = 0
        for tournament in self.tournaments.find():
            try:
                if tournament['id'] > max:
                    max = tournament['id']
            except:
                pass

        return max + 1


