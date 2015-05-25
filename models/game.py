import operator

class Game:

    def __init__(self, id, players, format):
        self.id = id
        self.players = players
        self.format = format

    def getVictor(self):
        return max(self.players.items(), key=operator.itemgetter(1))[0]

