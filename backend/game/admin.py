from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'incorrect_guesses', 'max_incorrect_guesses', 'state')
