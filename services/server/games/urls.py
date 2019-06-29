from django.urls import path
from .views import GameDetailView, LeaderboardView, GameRedirectView, CompetitionDetailView, GameListView

urlpatterns = [
    path('test', GameListView.as_view(), name='game-list'),
    path('<int:game_id>/leaderboard', LeaderboardView.as_view(), name='game-leaderboard'),
    path('<int:game_id>/competitions/<int:competition_id>', CompetitionDetailView.as_view(), name='competition-detail'),
    path('<int:game_id>', GameDetailView.as_view(), name='game-detail'),
    path('', GameListView.as_view(), name='games'),
]
