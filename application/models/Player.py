class Player:

    def __init__(self, id, name, life=20):
        self.id = id
        self.name = name
        self.life = life

    def get_games(self, all_games):
        games = []
        for game in all_games:
            if self.id in game.players.keys():
                games.append(game)

        return games

    def get_current_game(self, games):
        for game in games:
            if game.is_ongoing():
                return game

        return None

    def get_performance(self, games):
        performance = [0, 0]
        for game in games:
            if game.get_victor() == None:
                pass
            elif game.get_victor() == self.id:
                performance[0] += 1
            else:
                performance[1] += 1

        return performance

    def get_tournaments(self, all_tournaments):
        tournaments = []
        for tournament in all_tournaments:
            if self.id in tournament.players:
                tournaments.append(tournament)

        return tournaments
