import operator

class Game:

    def __init__(self, id, players, best_of, format):
        self.id = id
        self.players = players
        self.best_of = best_of
        self.format = format

    def get_victor(self):
        return max(self.players.items(), key=operator.itemgetter(1))[0]

    def is_ongoing(self):
        for player in self.players:
            if player.value() >= best_of/2:
                return False

        return True
