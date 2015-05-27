class Tournament:

    def __init__(self, id, name, format, players=[], games=[]):
        self.id = id
        self.name = name
        self.players = players
        self.games = games
        self.format = format

    def get_player_performance(self, player):
        performance = (0, 0)
        for game in self.games:
            if player.id in game.players.keys():
                if game.get_victor() == player.id:
                    performance[0] += 1

                offset = game.players[player.id]
                for player in game.players:
                    offset -= player.value()
                performance[1] += offset

        return performance


