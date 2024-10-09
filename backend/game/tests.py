from django.test import TestCase
from .models import Game

class GameModelTest(TestCase):
    def setUp(self):
        Game.objects.create(word='Python', max_incorrect_guesses=3)

    def test_game_creation(self):
        game = Game.objects.get(word='Python')
        self.assertEqual(game.word, 'Python')
        self.assertEqual(game.max_incorrect_guesses, 3)
        self.assertEqual(game.incorrect_guesses, 0)
        self.assertEqual(game.state, 'InProgress')
