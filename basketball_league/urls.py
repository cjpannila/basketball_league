from django.contrib import admin
from django.urls import path

from basketball_tournament import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('games/', views.get_all_games, name="get_all_games"),
    path('winnerteam/', views.get_winner_team, name="get_winner_team"),
    path('player/<int:player_id>/', views.get_player, name="get_player"),
    path('players/<int:team_id>/', views.get_players_in_team, name="get_players_in_team"),
    path('highperformingplayers/<int:team_id>/<int:percentile>/', views.get_players_in_avg_score_90th_percentile,
         name="get_players_in_avg_score_90th_percentile")
]
