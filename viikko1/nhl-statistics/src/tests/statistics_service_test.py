import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class testStatisticsService(unittest.TestCase):
    def setUp(self):
        self.service = StatisticsService(PlayerReaderStub())

    def test_search_returns_player_when_name_matches(self):
        player = self.service.search("Gretz")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Gretzky")

    def test_search_returns_exact_match(self):
        player = self.service.search("Semenko")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Semenko")

    def test_search_returns_none_when_player_not_in_service(self):
        player = self.service.search("Testi Testinen")
        self.assertIsNone(player)

    def test_team_returns_all_players_of_team(self):
        players = self.service.team("EDM")
        self.assertEqual(len(players), 3)
        names = [p.name for p in players]
        self.assertIn("Semenko", names)
        self.assertIn("Kurri", names)
        self.assertIn("Gretzky", names)

    def test_team_returns_empty_list_when_no_players(self):
        players = self.service.team("DDD")
        self.assertEqual(players, [])

    def test_top_returns_n_players_in_descending_order(self):
        top2 = self.service.top(2)
        self.assertEqual(len(top2), 3)
        self.assertEqual(top2[0].name, "Gretzky")
        self.assertEqual(top2[1].name, "Lemieux")

    def test_top_by_goals_returns_players_sorted_by_goals(self):
        top2_goals = self.service.top(2, SortBy.GOALS)
        self.assertEqual(len(top2_goals), 3)
        self.assertEqual(top2_goals[0].name, "Lemieux")
        self.assertEqual(top2_goals[1].name, "Yzerman")

    def test_top_by_assists_returns_players_sorted_by_assists(self):
        top2_assists = self.service.top(2, SortBy.ASSISTS)
        self.assertEqual(len(top2_assists), 3)
        self.assertEqual(top2_assists[0].name, "Gretzky")
        self.assertEqual(top2_assists[1].name, "Yzerman")

    def test_top_by_points_returns_players_sorted_by_points(self):
        top3_points = self.service.top(3, SortBy.POINTS)
        self.assertEqual(len(top3_points), 4)
        self.assertEqual(top3_points[0].name, "Gretzky")
        self.assertEqual(top3_points[1].name, "Lemieux")
        self.assertEqual(top3_points[2].name, "Yzerman")

    def test_top_without_sort_key_defaults_to_points(self):
        top2_default = self.service.top(2)
        top2_points = self.service.top(2)
        self.assertEqual(len(top2_default), 3)
        self.assertEqual(top2_default[0].name, top2_points[0].name)
        self.assertEqual(top2_default[1].name, top2_points[1].name)
        self.assertEqual(top2_default[0].name, "Gretzky")
        self.assertEqual(top2_default[1].name, "Lemieux")

