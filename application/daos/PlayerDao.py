from pymongo import MongoClient

from application.models.Player import Player

class PlayerDao:

    players = MongoClient().dev_db.players

    def create(self, player):
        return self.players.insert(player.__dict__)

    def retrieveAll(self):
        return self.players.find()

    def retrieveById(self, id):
        return self.players.find_one({'id': int(id)})

    def retrieveByName(self, name):
        return self.players.find_one({'name': name})

    def updateById(self, id, player):
        return self.players.update({'id': int(id)}, player.__dict__)

    def updateByName(self, name, player):
        return self.players.update({'name': name}, player.__dict__)

    def destroyById(self, id):
        return self.players.remove({'id': int(id)})

    def destroyByName(self, name):
        return self.players.remove({'name': name})


    def getValidId(self):
        max = 0
        for player in self.players.find():
            try:
                if player['id'] > max:
                    max = player['id']
            except:
                pass

        return max + 1
