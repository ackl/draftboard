import operator

class Game:

    def __init__(self, id, players, best_of, format):
        self.id = id
        self.players = players
        self.best_of = best_of
        self.format = format

    def get_victor(self):
        if self.is_ongoing():
            return None
        else:
            return max(self.players.items(), key=operator.itemgetter(1))[0]

    def is_ongoing(self):
        for player_wins in self.players.values():
            if player_wins > self.best_of/2:
                return False

        return True 
