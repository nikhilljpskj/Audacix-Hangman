from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'word', 'incorrect_guesses', 'max_incorrect_guesses', 'state']
