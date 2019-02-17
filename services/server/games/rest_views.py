from rest_framework import generics
from .serializers import GameSerializer, WODSerializer
from .models import Game, WOD

class GameListView(generics.ListCreateAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()


class GameDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()


class WODListView(generics.ListCreateAPIView):
    serializer_class = WODSerializer
    queryset = WOD.objects.all()


class WODDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WODSerializer
    queryset = WOD.objects.all()
