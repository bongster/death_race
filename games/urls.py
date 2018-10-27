from django.urls import path
from .views import GameDetailView, WODView, LeaderboardView, GameRedirectView, WODDetailView, CompetitionDetailView

urlpatterns = [
    path('<int:game_id>/leaderboard', LeaderboardView.as_view(), name='game-leaderboard'),
    path('<int:game_id>/wod/<int:pk>', WODDetailView.as_view(), name='game-wod-detail'),
    path('<int:game_id>/wod', WODView.as_view(), name='game-wod'),
    path('<int:game_id>/competitions/<int:competition_id>', CompetitionDetailView.as_view(), name='competition-detail'),
    path('<int:game_id>', GameDetailView.as_view(), name='game-detail'),
    path('', GameRedirectView.as_view(), name='games'),
]
