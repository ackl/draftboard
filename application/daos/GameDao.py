from pymongo import MongoClient

from application import db
from application.models.Game import Game

class GameDao:

    games = db.games

    def create(self, game):
        return self.games.insert(game.__dict__)

    def retrieveAll(self):
        return self.games.find()

    def retrieveById(self, id):
        return self.games.find_one({'id': int(id)})

    def updateById(self, id, game):
        return self.games.update({'id': int(id)}, game.__dict__)

    def destroyById(self, id):
        return self.games.remove({'id': int(id)})


    def getValidId(self):
        max = 0
        for game in self.games.find():
            try:
                if game['id'] > max:
                    max = game['id']
            except:
                pass

        return max + 1
