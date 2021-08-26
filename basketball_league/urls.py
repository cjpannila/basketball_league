from django.contrib import admin
from django.urls import path

from basketball_tournament import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('games/', views.get_all_games, name="get_all_games"),
    path('winnerteam/', views.get_winner_team, name="get_winner_team")
]
