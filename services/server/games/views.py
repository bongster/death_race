import logging

from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, ListView


from .models import Game, WOD2Game, WOD, Team2Game, Competition, Game2Sponsor
from teams.models import Team
from records.models import Record
from .forms import LeaderboardForm
from sponsors.models import Sponsor

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

class GameListView(ListView):
    model = Game
    template_name = 'game/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        team_type = form.data.get('team_type')
        sort_key = form.data.get('sort_key')

        team_list = Team.objects.prefetch_related('team2user_set__user').filter(
            id__in=Team2Game.objects.filter(
                game_id=game.id,
                is_active=True,
            ).values_list('team_id', flat=True),
        )

        competition_list = Competition.objects.filter(
            game_id=game.id,
            is_active=True,
        )

        if competition:
            competition_list = competition_list.filter(id=competition)

        wod_list = WOD.objects.filter(
            competition_id__in=competition_list.values_list('id', flat=True),
            is_active=True,
        )

        if team_type:
            team_list = team_list.filter(
                team_type=team_type
            )

        if division:
            team_list = team_list.filter(
                gender_type=division,
            )

        team_map = {team.id: team for team in team_list}

        leaderboard = {
            'header': ['type', 'name', 'point'],
            'data': []
        }

        wod_ids = [wod.id for wod in wod_list]
        if sort_key:
            sort_key = 2 + wod_ids.index(int(sort_key)) + 1
            print('sort_key: {}'.format(sort_key))
        else:
            sort_key = 2

        leaderboard['header'].extend([wod.name for wod in wod_list])

        for team in team_list:
            if team.team_type == 'individual':
                team_name = team.name
            else:
                team_name = '{} ({})'.format(
                    team.name,
                    ', '.join([
                        user.name for user in [
                            team2user.user for team2user in team.team2user_set.filter()
                        ]
                    ]),
                )
            data = [team.team_type.upper(), team_name , 0]
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
                data[2] += team_record['point']

                data.append(team_record['score'])

            leaderboard['data'].append(data)

        leaderboard['data'] = sorted(leaderboard['data'], key=lambda data: (data[sort_key] is 0, data[sort_key]))

        # set rank in code
        leaderboard['header'].insert(0, 'rank')
        point_rank_map = {}
        rank = 0;
        for d in leaderboard['data']:
            d_point = d[sort_key]
            if point_rank_map.get(d_point):
                d_rank = point_rank_map[d_point]
            else:
                rank = rank + 1
                point_rank_map[d_point] = rank
            d.insert(0, point_rank_map[d_point])

        if search:
            leaderboard['data'] = filter(lambda d: search in d[2], leaderboard['data'])

        context['team_map'] = team_map
        context['leaderboard'] = leaderboard
        context['form'] = form
        return context
