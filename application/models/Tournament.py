class Tournament:

    def __init__(self, id, name, format, players=[], matches=[]):
        self.id = id
        self.name = name
        self.players = players
        self.matches = matches
        self.format = format

    def get_player_performance(self, player):
        performance = (0, 0)
        for match in self.matches:
            if player.id in match.player_scores.keys():
                if match.get_victor() == player.id:
                    performance[0] += 1

                offset = match.player_scores[player.id]
                for player in match.player_scores:
                    offset -= player.value()
                performance[1] += offset

        return performance


