from django.db import models
from django.contrib.auth import get_user_model


class Team(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return str(self.name)


class Player(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    height = models.IntegerField(null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Game(models.Model):
    GAME_TYPES = [('FR', 'RoundOf16'), ('SR', 'RoundOf8'), ('SF', 'SemiFinal'), ('F', 'Final')]
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    winner_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    played_on = models.DateTimeField()
    game_type = models.CharField(max_length=2, choices=GAME_TYPES)

    def __str__(self):
        return str(f'{self.game_type.__str__()} | {self.team1.name} vs {self.team2.name} > {self.winner_team.name}')


class Coach(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    team = models.OneToOneField('Team', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class PlayerScore(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(blank=True)

    def __str__(self):
        return str(f'{self.player.name} on {self.game.played_on} scored {self.score}')


class TeamScore(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return str(f'{self.team.name} on {self.game.played_on} scored {self.score}')