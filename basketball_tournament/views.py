from django.shortcuts import render
from .models import Game, TeamScore, Team, Player, PlayerScore
from django.http import JsonResponse, HttpResponse
import json
import numpy as np


def home(request):
    games = Game.objects.all()
    return render(request, 'home.html', {
        'games': games,
    })


def get_all_games(request):
    response = []
    games = Game.objects.all()
    for game in games:
        response_data = {
            'id': game.id,
            'game_type': f'{game.game_type}',
            'team1': f'{game.team1.name}',
            'team2': f'{game.team2.name}',
            'team1_score': TeamScore.objects.filter(team_id__exact=game.team1_id)[0].score,
            'team2_score': TeamScore.objects.filter(team_id__exact=game.team2_id)[0].score,
            'winner_team': f'{game.winner_team.name}'
        }
        response.append(response_data)

    return HttpResponse(json.dumps(response), content_type="application/json")


def get_winner_team(request):
    final_game = Game.objects.filter(game_type__exact='F')[0]
    winner_team = Team.objects.get(id=final_game.winner_team_id)
    response_data = {
        'champion_team': winner_team.name
    }
    return JsonResponse(response_data, safe=False)


def get_player(request, player_id):
    player = Player.objects.get(id=player_id)
    response_data = get_player_details(player)
    return JsonResponse(response_data, safe=False)


def get_player_details(player):
    player_scores = PlayerScore.objects.filter(player__exact=player.id)
    num_of_games = 0
    sum_score = 0
    for player_score in player_scores:
        if player_score.score != 0:
            num_of_games += 1
            sum_score += player_score.score
    avg_score = 0
    if num_of_games > 0:
        avg_score = sum_score / num_of_games
    response_data = {
        'name': player.name,
        'team': player.team.name,
        'height': player.height,
        'num_of_games': num_of_games,
        'average_score': avg_score
    }
    return response_data


def get_players_in_team(request, team_id):
    players = Player.objects.filter(team_id__exact=team_id)
    response_data = []
    for player in players:
        player_details = get_player_details(player)
        response_data.append(player_details)
    return JsonResponse(response_data, safe=False)


def get_players_in_avg_score_90th_percentile(request, team_id, percentile):
    players = Player.objects.filter(team_id__exact=team_id)
    avg_list = []
    response_data = []
    for player in players:
        player_details = get_player_details(player)
        avg_score = player_details['average_score']
        avg_list.append(avg_score)
    benchmark = np.percentile(avg_list, percentile)
    print(f'percentile:{percentile} benchmark of team {Team.objects.get(id=team_id).name}: {benchmark}')
    print(f'List of scores of team {avg_list}')
    for player in players:
        player_details = get_player_details(player)
        avg_score = player_details['average_score']
        if avg_score > benchmark:
            response_data.append(player_details)
    return JsonResponse(response_data, safe=False)

