from rest_framework import serializers
from .models import Game, WOD

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Game
        fields=serializers.ALL_FIELDS


class WODSerializer(serializers.ModelSerializer):
    class Meta:
        model=WOD
        fields=serializers.ALL_FIELDS
