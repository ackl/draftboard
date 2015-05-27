import operator

class Match:

    def __init__(self, id, player_scores, best_of, format):
        self.id = id
        self.player_scores = player_scores
        self.best_of = best_of
        self.format = format

    def get_victor(self):
        if self.is_ongoing():
            return None
        else:
            return max(self.player_scores.items(), key=operator.itemgetter(1))[0]

    def is_ongoing(self):
        for player_wins in self.player_scores.values():
            if player_wins > self.best_of/2:
                return False

        return True

    def win_game(self, player_id):
        if player_id in self.player_scores and self.is_ongoing():
            self.player_scores[player_id] = self.player_scores[player_id] + 1

