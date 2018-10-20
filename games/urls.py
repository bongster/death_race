from django.urls import path
from .views import GameDetailView, WODView, LeaderboardView, GameRedirectView, WODDetailView

urlpatterns = [
    path('<int:game_id>/leaderboard', LeaderboardView.as_view(), name='game-leaderboard'),
    path('<int:game_id>/wod/<int:pk>', WODDetailView.as_view(), name='game-wod-detail'),
    path('<int:game_id>/wod', WODView.as_view(), name='game-wod'),
    path('<int:pk>', GameDetailView.as_view(), name='game-detail'),
    path('', GameRedirectView.as_view(), name='games'),
]
