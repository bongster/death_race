import logging

from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView

from .models import Game, WOD2Game, WOD

# Create your views here.

logger = logging.getLogger(__name__)


class GameRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'game-detail'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['pk'] = kwargs.get('pk') or 1
        return super().get_redirect_url(*args, **kwargs)

class GameDetailView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['game'] = Game.objects.get(pk=kwargs['pk'])
        print(context['game'])
        return context

class LeaderboardView(TemplateView):
    template_name = 'leaderboard/index.html'
    def get_context_data(self, **kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)
        print(context)
        context['game'] = Game.objects.get(pk=kwargs['game_id'])
        context['leaderboard'] = []
        return context

class WODView(TemplateView):
    template_name = 'wod/index.html'
    def get_context_data(self, **kwargs):
        context = super(WODView, self).get_context_data(**kwargs)
        game = Game.objects.get(pk=kwargs['game_id'])
        wod_ids = WOD2Game.objects.filter(
            game_id=game.id,
            is_ative=True,
        ).order_by('order').values_list('wod_id', flat=True)
        print(wod_ids)

        context['game'] = game
        wods = WOD.objects.filter(
            pk__in=wod_ids,
        )
        context_wods = {}
        for wod_id in wod_ids:
            wod = list(filter(lambda x: x.id == wod_id, wods))[0]
            context_wods[wod.id] = wod

        context['wods'] = context_wods

        return context

class WODDetailView(TemplateView):
    template_name = 'wod/index.html'
    def get_context_data(self, **kwargs):
        context = super(WODDetailView, self).get_context_data(**kwargs)
        context['game'] = Game.objects.get(pk=kwargs['game_id'])
        return context
