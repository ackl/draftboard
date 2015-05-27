from unittest import TestCase

from application import client
from application.models.Player import Player
from application.models.Match import Match
from application.models.Tournament import Tournament

class ModelTestCase(TestCase):

    def setUp(self):
        player_1 = Player(1, "Paulo")
        player_2 = Player(2, "Andrew")
        player_3 = Player(3, "Trampy")

        self.all_matches = []

        self.match_1 = Match(1, {1:2, 2:1}, 3, "Constructed/Standard")
        self.all_matches.append(self.match_1)
        self.match_2 = Match(2, {2:1, 3:2}, 3, "Limited/Booster Draft")
        self.all_matches.append(self.match_2)
        self.match_3 = Match(3, {1:2, 2:1}, 5, "Constructed/Modern")
        self.all_matches.append(self.match_3)

        self.player_1_matches = player_1.get_matches(self.all_matches)
        self.player_2_matches = player_2.get_matches(self.all_matches)
        self.player_3_matches = player_3.get_matches(self.all_matches)

        self.player_1_current_match = player_1.get_current_match(self.player_1_matches)
        self.player_2_current_match = player_2.get_current_match(self.player_2_matches)
        self.player_3_current_match = player_3.get_current_match(self.player_3_matches)

        self.player_1_performance = player_1.get_performance(self.player_1_matches)
        self.player_2_performance = player_2.get_performance(self.player_2_matches)
        self.player_3_performance = player_3.get_performance(self.player_3_matches)

        all_tournaments = []

        self.tournament = Tournament(1, "FNM Draft 2015", "Limited/Booster Draft", [1,2])
        all_tournaments.append(self.tournament)

        self.player_1_tournaments = player_1.get_tournaments(all_tournaments)
        self.player_2_tournaments = player_2.get_tournaments(all_tournaments)
        self.player_3_tournaments = player_3.get_tournaments(all_tournaments)


    def test_get_matches(self):
        self.assertEqual(self.player_1_matches, [self.match_1, self.match_3])
        self.assertEqual(self.player_2_matches, self.all_matches)
        self.assertEqual(self.player_3_matches, [self.match_2])

    def test_get_current_match(self):
        self.assertEqual(self.player_1_current_match, self.match_3)
        self.assertEqual(self.player_2_current_match, self.match_3)
        self.assertEqual(self.player_3_current_match, None)

    def test_get_performance(self):
        self.assertEqual(self.player_1_performance, [1, 0])
        self.assertEqual(self.player_2_performance, [0, 2])
        self.assertEqual(self.player_3_performance, [1, 0])

    def test_get_tournaments(self):
        self.assertEqual(self.player_1_tournaments, [self.tournament])
        self.assertEqual(self.player_2_tournaments, [self.tournament])
        self.assertEqual(self.player_3_tournaments, [])
