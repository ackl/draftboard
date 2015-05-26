from pymongo import MongoClient

from application.models.Player import Player

class PlayerDao:

    global players 
    players = MongoClient().dev_db.players

    def create(self, player):
        return players.insert(player.__dict__)

    def retrieveAll(self):
        return players.find()
    
    def retrieveById(self, id):
        return players.find_one({'id': int(id)})

    def retrieveByName(self, name):
        return players.find_one({'name': name})
    
    def updateById(self, id, player):
        return players.update({'id': int(id)}, player.__dict__)

    def updateByName(self, name, player):
        return players.update({'name': name}, player.__dict__)

    def destroyById(self, id):
        return players.remove({'id': int(id)})

    def destroyByName(self, name):
        return players.remove({'name': name})


    def getValidId(self):
        max = 0
        for player in players.find():
            try:
                if player['id'] > max:
                    max = player['id']
            except:
                pass

        return max + 1
