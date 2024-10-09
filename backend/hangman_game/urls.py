from django.contrib import admin
from django.urls import path, include
from game import views as game_views

urlpatterns = [
    path('', game_views.welcome),  
    path('admin/', admin.site.urls),
    path('game/', include('game.urls')),
]
