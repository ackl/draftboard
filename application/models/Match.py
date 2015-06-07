from application import db, get_socket

from MongoModel import MongoModel

import operator, json
socketio = get_socket()


class Match(MongoModel):

    collection = db.matches

    fields = [{
            'identifier': 'player_scores',
            'required': True,
            'type': dict
        },
        {
            # Best of value must obey
            # best_of = (number_of_players * n) + 1
            # where n is an integer
            'identifier': 'best_of',
            'required': True,
            'type': int,
            'default': 3
        },
        {
            'identifier': 'dead',
            'required': False,
        },
        {
            'identifier': 'format',
            'required': True,
            'type': str,
            'default': 'Standard'
        }]

    @classmethod
    def validate(cls, doc):
        super_validate = super(Match, cls).validate(doc)

        if super_validate is not True:
            return super_validate
        else:
            if (int(doc['best_of']) - 1)%len(json.loads(doc['player_scores'])) is not 0:
                return {"invalid_cause": "invalid_field_value", "fields": ['best_of (best_of - 1 must be a multiple of the number of players)']}
            else:
                return True

    def get_victor(self):
        if self.is_ongoing():
            return None
        else:
            return max(self.coerce_type('player_scores').items(), key=operator.itemgetter(1))[0]

    def is_ongoing(self):
        for player_wins in self.coerce_type('player_scores').values():
            if player_wins >= self.best_of/2.0:
                return False
        return True

    def win_game(self, player_id):
        self.dead = []
        player_id = str(player_id)
        if player_id in self.player_scores and self.is_ongoing():
            self.player_scores[player_id] = self.player_scores[player_id] + 1
            socketio.emit('win_game', {
                'player_id': player_id,
                'score': self.player_scores[player_id],
                'finished': self.is_ongoing()
            })


        from Player import Player
        for player_id in self.player_scores.keys():
            Player.query({'_id': player_id}).update({'life': 20})

        self.update()

    def generate_json(self):
        from Player import Player
        json_dict = MongoModel.generate_json(self)

        if not self.is_ongoing():
            json_dict['victor'] = self.get_victor()
        json_dict['is_ongoing'] = self.is_ongoing()

        players = self.coerce_type('player_scores').keys()
        json_dict['players'] = [Player.query({'_id': key}).__dict__ for key in players]

        for player in json_dict['players']:
            player['score'] = json_dict['player_scores'][player['_id']]

        json_dict.pop('player_scores', None)
        return json_dict

    def player_died(self, player_id):
        if hasattr(self, 'dead'):
            self.dead.append(player_id)
        else:
            self.dead = [player_id]

        self.update({'dead': self.dead})
        if len(self.dead) is len(self.player_scores)-1:
            winner = set(self.player_scores.keys()) - set(self.dead)
            winner = next(iter(winner))
            self.win_game(winner)

