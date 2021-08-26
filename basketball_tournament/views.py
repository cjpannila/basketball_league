from django.shortcuts import render
from .models import Game, TeamScore
from django.http import JsonResponse


def home(request):
    games = Game.objects.all()
    team_scores = TeamScore.objects.all()
    return render(request, 'home.html', {
        'games': games,
        'team_scores': team_scores,
    })


def get_all_games(request):
    return JsonResponse({'foo': f'{1}'})
