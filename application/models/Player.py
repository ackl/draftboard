class Player:

    def __init__(self, id, name, life=20):
        self.id = id
        self.name = name
        self.life = life

    def get_matches(self, all_matches):
        matches = []
        for match in all_matches:
            if self.id in match.players.keys():
                matches.append(match)

        return matches

    def get_current_match(self, matches):
        for match in matches:
            if match.is_ongoing():
                return match

        return None

    def get_performance(self, matches):
        performance = [0, 0]
        for match in matches:
            if match.get_victor() == None:
                pass
            elif match.get_victor() == self.id:
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
