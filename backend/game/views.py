import random
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Game
from .serializers import GameSerializer
from django.http import JsonResponse
import logging

def welcome(request):
    return JsonResponse({"message": "Audacic... Hangman"})

def get_word_state(self):
    return ''.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

class GameViewSet(viewsets.ViewSet):
    WORDS = ["Hangman", "Python", "Audacix", "Bottle", "Pen"]

    @action(detail=False, methods=['post'], url_path='new')
    def new_game(self, request):
        try:
            word = random.choice(self.WORDS).lower()
            max_incorrect_guesses = len(word) // 2
            
            game = Game.objects.create(
                word=word,
                max_incorrect_guesses=max_incorrect_guesses,
                guessed_letters=''
            )
            logging.info(f"New game created with id: {game.id}")
            return Response({'id': game.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(f"Error creating new game: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=['get'], url_path='')
    def game_state(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            if game.state == 'Lost':
                current_word = game.word  
            else:
                current_word = game.get_word_state()  
            return Response({
                'state': game.state,
                'current_word': current_word,
                'incorrect_guesses': game.incorrect_guesses,
                'max_incorrect_guesses': game.max_incorrect_guesses,
            }, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found.'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['post'], url_path='guess')
    def guess(self, request, pk=None):
        letter = request.data.get('letter', '').lower()
        try:
            game = Game.objects.get(pk=pk)

            if game.state != 'InProgress':
                return Response({'error': 'Game is already finished.'}, status=status.HTTP_400_BAD_REQUEST)

            if letter in game.word and letter not in game.guessed_letters:
                game.guessed_letters += letter
            else:
                if letter not in game.word:
                    game.incorrect_guesses += 1

            
            if game.incorrect_guesses >= game.max_incorrect_guesses:
                game.state = 'Lost'
            elif set(game.word).issubset(set(game.guessed_letters)):
                game.state = 'Won'

            game.save()
            return Response({
                'state': game.state,
                'current_word': game.get_word_state(),
                'incorrect_guesses': game.incorrect_guesses,
                'max_incorrect_guesses': game.max_incorrect_guesses,
                'correct_guess': letter in game.word,
            }, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found.'}, status=status.HTTP_404_NOT_FOUND)
