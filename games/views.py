import logging

from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView

from .models import Game, WOD2Game, WOD, Team2Game, Team, Record, Competition, Sponsor, Game2Sponsor
from .forms import LeaderboardForm

# Create your views here.

logger = logging.getLogger(__name__)


class DefaultContextMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs.get('game_id'):
            context['game_id'] = kwargs['game_id']
            context['game'] = Game.objects.get(id=kwargs['game_id'])
            context['competitions'] = Competition.objects.filter(
                game_id=context['game'].id,
                is_active=True,
            ).order_by('id')
            context['sponsors'] = Sponsor.objects.filter(
                id__in=Game2Sponsor.objects.filter(game_id=context['game'].id).values_list('sponsor_id', flat=True),
                is_active=True,
            )
        if kwargs.get('competition_id'):
            context['competition_id'] = kwargs['competition_id']
            context['competition'] = Competition.objects.get(pk=context['competition_id'])

        print('call default context')
        return context


class GameRedirectView(DefaultContextMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'game-detail'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['game_id'] = kwargs.get('game_id') or 1
        return super().get_redirect_url(*args, **kwargs)


class CompetitionDetailView(DefaultContextMixin, TemplateView):
    template_name = 'competition/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competition = context['competition'] # Competition.objects.get(pk=kwargs['pk'])

        wods = WOD.objects.filter(
            is_active=True,
            competition_id=competition.id,
        )

        wod_ids = wods.values_list('id', flat=True)

        context_wods = {}
        for wod_id in wod_ids:
            wod = list(filter(lambda x: x.id == wod_id, wods))[0]
            context_wods[wod_id] = wod

        context['wods'] = context_wods

        return context


class GameDetailView(DefaultContextMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)

        return context


class LeaderboardView(DefaultContextMixin, TemplateView):
    template_name = 'leaderboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)
        game = context['game']
        # get teams list included in game
        form = LeaderboardForm(game.id, self.request.GET or None)
        division = form.data.get('division')
        search = form.data.get('search')
        competition = form.data.get('competition')

        team_list = Team.objects.filter(
            id__in=Team2Game.objects.filter(
                game_id=game.id,
                is_active=True,
            )
        )

        competition_list = Competition.objects.filter(
            game_id=game.id,
            is_active=True,
        )

        wod_list = WOD.objects.filter(
            competition_id__in=competition_list.values_list('id', flat=True),
            is_active=True,
        )

        if search:
            team_list = team_list.filter(
                name__contains=search,
            )

        if division:
            team_list = team_list.filter(
                gender_type=division,
            )

        if competition:
            competition_list.filter(id=competition)

        team_map = {team.id: team for team in team_list}

        leaderboard = {
            'header': ['name', 'point'],
            'data': []
        }

        wod_ids = [wod.id for wod in wod_list]

        leaderboard['header'].extend([wod.name for wod in wod_list])

        for team in team_list:
            data = [team.name, 0]
            team_records = {record['wod_id']: record for record in Record.objects.filter(
                team_id=team.id,
                is_active=True,
            ).values('wod_id', 'score', 'point')}
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

        context['team_map'] = team_map
        context['leaderboard'] = leaderboard
        context['form'] = form
        return context
