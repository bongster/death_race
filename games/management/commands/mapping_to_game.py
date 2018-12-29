from django.core.management.base import BaseCommand, CommandError

from games.models import Game, Team, Game2Team


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--game_id',
            dest='game_id',
            type=int
        )

    def handle(self, *args, **options):
        print(options['game_id'])
        g = Game.objects.get(pk=options['game_id'])

        for t in Team.objects.filter(
            is_active=True
        ):
            g2t = Game2Team(
                team_id=t.id,
                game_id=g.id,
                is_active=True,
            )
            g2t.save()