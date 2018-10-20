import logging

from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView

from .models import Game, WOD2Game, WOD, Team2Game, Team, Record
from .forms import LeaderboardForm

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
        game = Game.objects.get(pk=kwargs['game_id'])
        # get teams list included in game
        form = LeaderboardForm(game.id, self.request.GET or None)
        division = form.data.get('division')
        search = form.data.get('search')

        team_list = Team.objects.filter(
            id__in=Team2Game.objects.filter(
                game_id=game.id,
            )
        )

        if search:
            team_list = team_list.filter(
                name__contains=search,
            )

        if division:
            team_list = team_list.filter(
                gender_type=division,
            )
        
        team_map = { team.id: team for team in team_list }

        wods = WOD.objects.filter(
            id__in=WOD2Game.objects.filter(
                game_id=game.id
            )
        )

        leaderboard = {
            'header': ['name', 'point'],
            'data': []
        }
        
        wod_ids = [ wod.id for wod in wods ]
        
        leaderboard['header'].extend([ wod.name for wod in wods ])

        for team in team_list:
            data = [ team.name, 0 ]
            team_records = { record['wod_id']: record for record in Record.objects.filter(
                team_id=team.id,
                is_ative=True,
            ).values('wod_id', 'score', 'point') }
            for wod_id in wod_ids:
                team_record = team_records.get(wod_id) or dict(
                    score='',
                    point=0,
                )
                team_record['score']
                data[1] += team_record['point']
                
                data.append(team_record['score'])
            
            leaderboard['data'].append(data)

        # TODO: sort by point
        sorted(leaderboard['data'], key=lambda data: data[1], reverse=True)
        # print(leaderboard)

        # print(form.clean().search)
        # print(form.competition)
        # print(form.division)

        if form.is_valid():
            print(form.cleaned_data)
            
        context['game'] = game
        context['team_map'] = team_map
        context['leaderboard'] = leaderboard
        context['form'] = form
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
            context_wods[wod_id] = wod

        context['wods'] = context_wods

        return context

class WODDetailView(TemplateView):
    template_name = 'wod/index.html'
    def get_context_data(self, **kwargs):
        context = super(WODDetailView, self).get_context_data(**kwargs)
        context['game'] = Game.objects.get(pk=kwargs['game_id'])
        return context
