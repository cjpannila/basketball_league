from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from basketball_tournament.models import Team, Coach, Player, Game, PlayerScore, TeamScore
from faker import Faker

TEAM_NAMES = [
    'team1',
    'team2',
    'team3',
    'team4',
    'team5',
    'team6',
    'team7',
    'team8',
    'team9',
    'team10'
]


class Command(BaseCommand):
    def teamFake(self):
        fake = Faker()
        Team.objects.all().delete();
        for t in range(10):
            team = Team(name=fake.lexify(text='???????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
            team.save()
            self.stdout.write(f'Team added : {team.name}')

    def handle(self, *args, **options):
        fake = Faker()
        #self.teamFake()
        Team.objects.all().delete()
        for team_name in TEAM_NAMES:
            team = Team(name=team_name)
            team.save()
            self.stdout.write(f'Team added : {team.name}')
        Player.objects.all().delete()
        for team in Team.objects.all():
            self.stdout.write(f'{team.name}, {team.id}')
            for p in range(10):
                player = Player(name=f'player{p}_{team.name}', height=fake.random_int(min=170, max=255, step=1), team_id=team.id)
                player.save()
                self.stdout.write(f'Player added : {player.__str__()}')
