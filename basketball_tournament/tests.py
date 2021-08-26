from django.test import TestCase
from .models import Team
import requests


class AppTest(TestCase):

    def test_games(self):
        response = requests.get('http://localhost:8000/games/')
        games = response.json()
        self.assertEqual(response.status_code, 200, 'response status incorrect')
        self.assertEqual(len(games), 15, 'game count incorrect')

    def test_winner_team(self):
        response = requests.get('http://localhost:8000/winnerteam/')
        winner = response.json()
        winner_team = winner['champion_team']
        print(winner_team)
        self.assertEqual(response.status_code, 200, 'response status incorrect')
        self.assertIsNotNone(winner_team)

    def test_player(self):
        response = requests.get('http://localhost:8000/player/3595/')
        player = response.json()
        player_name = player['name']
        average_score = player['average_score']
        print(player_name, average_score)
        self.assertEqual(response.status_code, 200, 'response status incorrect')
        self.assertIsNotNone(player_name)
        self.assertIsNotNone(average_score)

    def test_players(self):
        response = requests.get('http://localhost:8000/players/440/')
        players = response.json()
        self.assertEqual(response.status_code, 200, 'response status incorrect')
        self.assertEqual(len(players), 10, 'players count incorrect')

    def test_players_percentile(self):
        response = requests.get('http://localhost:8000/highperformingplayers/440/90')
        players = response.json()
        self.assertEqual(response.status_code, 200, 'response status incorrect')
        self.assertIsNotNone(players)

    def test_players_50th_percentile(self):
        response = requests.get('http://localhost:8000/highperformingplayers/440/90')
        players = response.json()
        self.assertEqual(response.status_code, 200, 'response status incorrect')
        self.assertIsNotNone(players)

