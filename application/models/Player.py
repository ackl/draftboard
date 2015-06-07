from application import db, socketio

from MongoModel import MongoModel
from Match import Match


class Player(MongoModel):

    collection = db.players

    fields = [{
            'identifier': 'name',
            'required': True,
            'type': str
        },
        {
            'identifier': 'life',
            'required': True,
            'type': int,
            'default': 20
        }]

    def get_matches(self):
        return [match for match in Match.query() if str(self._id) in match.player_scores.keys()]

    def get_current_match(self):
        for match in self.get_matches():
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

    def generate_json(self):
        json_dict = MongoModel.generate_json(self)

        if self.get_current_match() is not None:
            json_dict['current_match'] = self.get_current_match().__dict__

        return json_dict

    def update(self, doc):
        """Synchronise the model's attributes to the
        corresponding mongodb document. Call player_died
        on the current match model if the life field value
        is 0.
        """
        MongoModel.update(self, doc)
        socketio.emit('response', {'player_id': str(self._id), 'life': self.life})
        if self.life is 0:
            match = self.get_current_match()
            if match is not None:
                match.player_died(self._id)

        return self
