from pymongo import MongoClient

from application import db
from application.models.Player import Player
from bson.objectid import ObjectId

class PlayerDao:

    players = db.players

    #def create(self, player):
        #return self.players.insert(player.__dict__)

    def create(self, name, life=20):
        player_id = self.players.insert({'name': name, 'life': life})
        return self.retrieveById(player_id)

    def retrieveAll(self):
        return self.players.find()

    def retrieveById(self, id):
        id = ObjectId(id)
        player_doc = self.players.find_one({'_id': id})
        player = Player(id, player_doc['name'], player_doc['life'])
        return player
        #return self.players.find_one({'_id': id})

    def retrieveByName(self, name):
        return self.players.find_one({'name': name})

    def updateById(self, id, player):
        id = ObjectId(id)
        return self.players.update({'_id': id}, player.__dict__)

    def updateLifeById(self, id, life):
        id = ObjectId(id)
        return self.players.update({'_id': id}, {"$set": {"life": life}}, upsert=False)

    def updateByName(self, name, player):
        return self.players.update({'name': name}, player.__dict__)

    def destroyById(self, id):
        return self.players.remove({'_id': int(id)})

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
