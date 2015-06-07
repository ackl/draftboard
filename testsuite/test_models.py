from unittest import TestCase

from application import client, db
from application.models.Player import Player
from application.models.Match import Match
from application.models.MongoModel import MongoModel
from application.models.Tournament import Tournament


class ModelTestCase(TestCase):

    #def setUp(self):

        #self.all_matches = []

        #self.match_1 = Match(1, {1:2, 2:1}, 3, "Constructed/Standard")
        #self.all_matches.append(self.match_1)
        #self.match_2 = Match(2, {2:1, 3:2}, 3, "Limited/Booster Draft")
        #self.all_matches.append(self.match_2)
        #self.match_3 = Match(3, {1:2, 2:1}, 5, "Constructed/Modern")
        #self.all_matches.append(self.match_3)

        #self.player_1_matches = player_1.get_matches(self.all_matches)
        #self.player_2_matches = player_2.get_matches(self.all_matches)
        #self.player_3_matches = player_3.get_matches(self.all_matches)
        #self.player_4_matches = player_4.get_matches(self.all_matches)

        #self.player_1_current_match = player_1.get_current_match(self.player_1_matches)
        #self.player_2_current_match = player_2.get_current_match(self.player_2_matches)
        #self.player_3_current_match = player_3.get_current_match(self.player_3_matches)
        #self.player_4_current_match = player_4.get_current_match(self.player_4_matches)

        #self.player_1_performance = player_1.get_performance(self.player_1_matches)
        #self.player_2_performance = player_2.get_performance(self.player_2_matches)
        #self.player_3_performance = player_3.get_performance(self.player_3_matches)
        #self.player_4_performance = player_4.get_performance(self.player_4_matches)

        #all_tournaments = []

        #self.tournament = Tournament(1, "FNM Draft 2015", "Limited/Booster Draft", [1,2])
        #all_tournaments.append(self.tournament)

        #self.player_1_tournaments = player_1.get_tournaments(all_tournaments)
        #self.player_2_tournaments = player_2.get_tournaments(all_tournaments)
        #self.player_3_tournaments = player_3.get_tournaments(all_tournaments)
        #self.player_4_tournaments = player_4.get_tournaments(all_tournaments)


    def test_new_player_defaults(self):
        player = Player({'_id': '1', 'name': 'Paulo'})
        for field_id in player.get_fields_with_defaults():
            assert getattr(player, field_id) is player.get_default_value(field_id)

    def test_new_player_has_20_life(self):
        player_1 = Player({'_id': '1'})
        assert player_1.life is 20
    #def test_get_matches(self):
        #"""Retrieving a list of matches that involve a player."""
        #assert self.player_1_matches == [self.match_1, self.match_3], 'more than one match'
        #assert self.player_2_matches == self.all_matches, 'all matches'
        #assert self.player_3_matches == [self.match_2], 'one match'
        #assert self.player_4_matches == [], 'no matches'

    #def test_get_current_match(self):
        #"""Retrieve the ongoing match for a player, if any."""
        #assert self.player_1_current_match == self.match_3, 'ongoing match'
        #assert self.player_3_current_match ==  None, 'no ongoing match'
        #assert self.player_4_current_match == None, 'no matches'

    #def test_get_performance(self):
        #"""Calculate performance (wins, losses) for a player."""
        #assert self.player_2_performance == [0, 2], 'ongoing match'
        #assert self.player_3_performance == [1, 0], 'no ongoing match'
        #assert self.player_4_performance == [0, 0], 'no matches'

    #def test_get_tournaments(self):
        #"""Retrieve a list of tournaments that involve a player."""
        #assert self.player_1_tournaments == [self.tournament], 'one tournament'
        #assert self.player_3_tournaments ==  [], 'no tournaments'
