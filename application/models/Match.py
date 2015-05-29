from application import db

from MongoModel import MongoModel

import operator, json


class Match(MongoModel):

    collection = db.matches

    fields = [{
            'identifier': 'player_scores',
            'required': True,
            'type': dict
        },
        {
            'identifier': 'best_of',
            'required': True,
            'type': int,
            'default': 3
        },
        {
            'identifier': 'format',
            'required': True,
            'type': str,
            'default': 'Standard'
        }]

    def get_victor(self):
        if self.is_ongoing():
            return None
        else:
            return max(self.coerce_type('player_scores').items(), key=operator.itemgetter(1))[0]

    def is_ongoing(self):
        for player_wins in self.coerce_type('player_scores').values():
            if player_wins > self.best_of/2:
                return False
        return True

    def win_game(self, player_id):
        if player_id in self.player_scores and self.is_ongoing():
            self.player_scores[player_id] = self.player_scores[player_id] + 1

    def json_helper(self):
        from Player import Player
        extra_json = {"is_ongoing": self.is_ongoing()}
        if not self.is_ongoing():
            extra_json["victor"] = self.get_victor()

        players = self.coerce_type('player_scores').keys()
        extra_json['players'] = [Player.query({'_id': key}).__dict__ for key in players]

        return extra_json

