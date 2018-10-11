from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class GameView(TemplateView):
    template_name = 'game.html'
