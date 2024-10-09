from django.urls import path
from .views import GameViewSet

urlpatterns = [
    path('new/', GameViewSet.as_view({'post': 'new_game'}), name='new_game'),
    path('<int:pk>/', GameViewSet.as_view({'get': 'game_state'}), name='game_state'),
    path('<int:pk>/guess/', GameViewSet.as_view({'post': 'guess'}), name='make-guess'),
]
