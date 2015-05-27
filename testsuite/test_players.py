from unittest import TestCase

from application import client 
from application.models.Player import Player
from application.models.Game import Game
from application.models.Tournament import Tournament

class ModelTestCase(TestCase):

    def setUp(self):
        player_1 = Player(1, "Paulo")
        player_2 = Player(2, "Andrew")
        player_3 = Player(3, "Trampy")

        self.all_games = []

        self.game_1 = Game(1, {1:2, 2:1}, 3, "Constructed/Standard")
        self.all_games.append(self.game_1)
        self.game_2 = Game(2, {2:1, 3:2}, 3, "Limited/Booster Draft")
        self.all_games.append(self.game_2)
        self.game_3 = Game(3, {1:2, 2:1}, 5, "Constructed/Modern")
        self.all_games.append(self.game_3)

        self.player_1_games = player_1.get_games(self.all_games)
        self.player_2_games = player_2.get_games(self.all_games)
        self.player_3_games = player_3.get_games(self.all_games)

        self.player_1_current_game = player_1.get_current_game(self.player_1_games)
        self.player_2_current_game = player_2.get_current_game(self.player_2_games)
        self.player_3_current_game = player_3.get_current_game(self.player_3_games)

        self.player_1_performance = player_1.get_performance(self.player_1_games)
        self.player_2_performance = player_2.get_performance(self.player_2_games)
        self.player_3_performance = player_3.get_performance(self.player_3_games)

        all_tournaments = []

        self.tournament = Tournament(1, "FNM Draft 2015", "Limited/Booster Draft", [1,2])
        all_tournaments.append(self.tournament)

        self.player_1_tournaments = player_1.get_tournaments(all_tournaments)
        self.player_2_tournaments = player_2.get_tournaments(all_tournaments)
        self.player_3_tournaments = player_3.get_tournaments(all_tournaments)
        

    def test_get_games(self):
        self.assertEqual(self.player_1_games, [self.game_1, self.game_3])
        self.assertEqual(self.player_2_games, self.all_games)
        self.assertEqual(self.player_3_games, [self.game_2])

    def test_get_current_game(self):
        self.assertEqual(self.player_1_current_game, self.game_3)
        self.assertEqual(self.player_2_current_game, self.game_3)
        self.assertEqual(self.player_3_current_game, None)

    def test_get_performance(self):
        self.assertEqual(self.player_1_performance, [1, 0])
        self.assertEqual(self.player_2_performance, [0, 2])
        self.assertEqual(self.player_3_performance, [1, 0])

    def test_get_tournaments(self):
        self.assertEqual(self.player_1_tournaments, [self.tournament])
        self.assertEqual(self.player_2_tournaments, [self.tournament])
        self.assertEqual(self.player_3_tournaments, [])
