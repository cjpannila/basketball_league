from django.core.management.base import BaseCommand
from basketball_tournament.models import Team, Coach, Player, Game, PlayerScore, TeamScore
from datetime import datetime
from django.utils import timezone
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
    'team10',
    'team11',
    'team12',
    'team13',
    'team14',
    'team15',
    'team16'
]


class Command(BaseCommand):

    def deletExistingRecords(self):
        # delete existing records
        Team.objects.all().delete()
        Player.objects.all().delete()
        Coach.objects.all().delete()
        Game.objects.all().delete()
        PlayerScore.objects.all().delete()
        TeamScore.objects.all().delete()

    def addTeamsPlayersAndCoach(self):
        fake = Faker()
        # add team records
        for team_name in TEAM_NAMES:
            team = Team(name=team_name)
            team.save()
            self.stdout.write(f'Team added : {team.name}')
        for team in Team.objects.all():
            self.stdout.write(f'For team {team.name}, {team.id}')
            # add coach record
            coach = Coach(name=f'coach_name_{team.name}', team_id=team.id)
            coach.save()
            self.stdout.write(f'Coach added : {coach.__str__()}')
            # add player records
            for p in range(10):
                player = Player(name=f'player_name_{p + 1}_{team.name}',
                                height=fake.random_int(min=170, max=255, step=1),
                                team_id=team.id)
                player.save()
                self.stdout.write(f'Player added : {player.__str__()}')

    def addGameRecords(self, game_round, round_team_names):
        fake = Faker()
        # add game records first round
        for g in range(int(len(round_team_names) / 2)):
            team1name = round_team_names[g]
            team2name = round_team_names[len(round_team_names) - 1 - g]
            team1 = Team.objects.get(name__exact=team1name)
            team2 = Team.objects.get(name__exact=team2name)
            game = Game(team1_id=team1.id, team2_id=team2.id, played_on=timezone.now(), game_type=game_round)
            game.save()
            self.stdout.write(f'Game added {game.game_type} | {game.team1.name} vs {game.team2.name}')
        # add scores and set winner for first round games
        for game in Game.objects.filter(game_type__exact=game_round):
            # add scores of individuals and team1
            team1_score_val = self.addScoresOfPlayersAndTeam(game.id, game.team1_id)
            # add scores of individuals and team2
            team2_score_val = self.addScoresOfPlayersAndTeam(game.id, game.team2_id)
            if team1_score_val > team2_score_val:
                game.winner_team_id = game.team1_id
            else:
                game.winner_team_id = game.team2_id
            game.save()
            self.stdout.write(f'Game scores added {game.game_type} |' +
                              f'{game.team1.name}({team1_score_val}) vs {game.team2.name}({team2_score_val})' +
                              f'> {game.winner_team.name}')

    def getWinnerTeamNames(self, game_round):
        winner_team_names = []
        for game in Game.objects.filter(game_type__exact=game_round):
            winner_team_names.append(Team.objects.get(id=game.winner_team_id).name)
        return winner_team_names

    def addScoresOfPlayersAndTeam(self, game_id, team_id):
        fake = Faker()
        team_score_val = 0
        for player in Player.objects.filter(team_id__exact=team_id):
            player_score = PlayerScore(game_id=game_id, player_id=player.id,
                                       score=fake.random_int(min=0, max=10, step=1))
            team_score_val = team_score_val + player_score.score
            player_score.save()
        team_score = TeamScore(team_id=team_id, game_id=game_id, score=team_score_val)
        team_score.save()
        return team_score_val

    def handle(self, *args, **options):
        # delete existing records
        self.deletExistingRecords()
        # add records to database
        self.addTeamsPlayersAndCoach()
        self.addGameRecords(game_round='FR', round_team_names=TEAM_NAMES)
        winner_team_names_fr = self.getWinnerTeamNames(game_round='FR')
        self.addGameRecords(game_round='SR', round_team_names=winner_team_names_fr)
        winner_team_names_sr = self.getWinnerTeamNames(game_round='SR')
        self.addGameRecords(game_round='SF', round_team_names=winner_team_names_sr)
        winner_team_names_sf = self.getWinnerTeamNames(game_round='SF')
        self.addGameRecords(game_round='F', round_team_names=winner_team_names_sf)
        winner_team_names_f = self.getWinnerTeamNames(game_round='F')
        self.stdout.write(f'Champion team: {winner_team_names_f[0]}')

    def handleX(self, *args, **options):
        self.getWinnerTeamNames(game_round='FR')
