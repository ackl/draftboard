from pymongo import MongoClient

from application import db
from application.models.Match import Match

class MatchDao:

    matches = db.matches

    def create(self, match):
        return self.matches.insert(match.__dict__)

    def retrieveAll(self):
        return self.matches.find()

    def retrieveById(self, id):
        return self.matches.find_one({'id': int(id)})

    def updateById(self, id, match):
        return self.matches.update({'id': int(id)}, match.__dict__)

    def destroyById(self, id):
        return self.matches.remove({'id': int(id)})


    def getValidId(self):
        max = 0
        for match in self.matches.find():
            try:
                if match['id'] > max:
                    max = match['id']
            except:
                pass

        return max + 1
