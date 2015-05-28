from application import db

from MongoModel import MongoModel


class Player(MongoModel):

    collection = db.players

    fields = [{
            'identifier': 'name',
            'required': True
        },
        {
            'identifier': 'life',
            'required': True,
            'default': 20
        }]

    def get_matches(self, all_matches):
        matches = []
        for match in all_matches:
            if self.id in match.player_scores.keys():
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
