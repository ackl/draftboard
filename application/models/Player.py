class Player:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.life = 20

    def getGames(self, all_games):
        games = []
        for game in all_games:
            if self in game.players.keys() :
                games.append(game)

        return games


