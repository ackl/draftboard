from pymongo import MongoClient

from application.models.Game import Game

class GameDao:

    global games
    games = MongoClient().dev_db.games

    def create(self, game):
        return games.insert(game.__dict__)

    def retrieveAll(self):
        return games.find()

    def retrieveById(self, id):
        return games.find_one({'id': int(id)})

    def updateById(self, id, game):
        return games.update({'id': int(id)}, game.__dict__)

    def destroyById(self, id):
        return games.remove({'id': int(id)})


    def getValidId(self):
        max = 0
        for game in games.find():
            try:
                if game['id'] > max:
                    max = game['id']
            except:
                pass

        return max + 1
