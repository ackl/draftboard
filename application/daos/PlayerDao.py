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
        player_docs = self.players.find()
        player_objects = []
        for doc in player_docs:
            player_objects.append(Player(doc['_id'], doc['name'], doc['life']))

        return player_objects

    def retrieveById(self, id):
        id = ObjectId(id)
        player_doc = self.players.find_one({'_id': id})
        player = Player(id, player_doc['name'], player_doc['life'])

        return player

    def retrieveByName(self, name):
        player_doc = self.players.find_one({'name': name})
        player = Player(player_doc['_id'], name, player_doc['life'])

        return player

    def updateById(self, id, player):
        id = ObjectId(id)

        return self.players.update({'_id': id}, player.__dict__)

    def updateByName(self, name, player):
        return self.players.update({'name': name}, player.__dict__)

    def updateLifeById(self, id, life):
        id = ObjectId(id)

        return self.players.update({'_id': id}, {"$set": {"life": life}})

    def updateNameById(self, id, name):
        id = ObjectId(id)

        return self.players.update({'_id':id}, {"$set": {"name": name}})

    def destroyById(self, id):
        games = self.retrieveById(id).get_games(GameDao.retrieveAll())
        for game in games:
            GameDao().destroyById(str(game.id))

        return self.players.remove({'_id': ObjectId(id)})

    def destroyByName(self, name):
        games = self.retrieveByName(name).get_games(GameDao.retrieveAll())
        for game in games:
            GameDao().destroyById(str(game.id))

        return self.players.remove({'name': name})

