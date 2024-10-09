from django.db import models

class Game(models.Model):
    word = models.CharField(max_length=100)
    max_incorrect_guesses = models.IntegerField()
    guessed_letters = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=20, default='InProgress')
    incorrect_guesses = models.IntegerField(default=0)

    def get_word_state(self):
        return ''.join([letter if letter in self.guessed_letters else '_' for letter in self.word])