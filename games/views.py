from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView

# Create your views here.


class GameRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'game-detail'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['pk'] = kwargs.get('pk') or 1
        return super().get_redirect_url(*args, **kwargs)

class GameView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        return context

class LeaderboardView(TemplateView):
    template_name = 'leaderboard/index.html'

class WODView(TemplateView):
    template_name = 'wod/index.html'
