from django.urls import path
from .views import GameView, WODView, LeaderboardView, GameRedirectView

urlpatterns = [
    path('<int:pk>/leaderboard', LeaderboardView.as_view(), name='game-leaderboard'),
    path('<int:pk>/wod', WODView.as_view(), name='game-wod'),
    path('<int:pk>', GameView.as_view(), name='game-detail'),
    path('', GameRedirectView.as_view(), name='games'),
]

