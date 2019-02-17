
from django.urls import path, include

'''
    TODO: definition using api
    sponsers/
    games/
    teams/
    wods/
'''

from games.rest_views import GameListView, GameDetailView, WODListView, WODDetailView


urlpatterns = [
    path('wods/<int:pk>', WODDetailView.as_view()),
    path('wods', WODListView.as_view()),
    path('games/<int:pk>', GameDetailView.as_view()),
    path('games', GameListView.as_view()),
    path('sponsors', include('sponsors.urls')),
    path('teams', include('teams.urls')),
]