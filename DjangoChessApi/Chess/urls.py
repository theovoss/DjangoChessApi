from django.urls import path

from DjangoChessApi.Chess import all_views as views
from DjangoChessApi.Chess.views.GameListView import GameListView
from DjangoChessApi.Chess.views.UserListView import UserListView


urlpatterns = [
    path('', views.home, name="home"),
    # Configurations
    path('configure/', views.create_configuration, name="configure"),
    path('configure/<int:game_type_id>/', views.configuration, name="configure-edit"),
    path(
        'configure/<int:game_type_id>/board',
        views.configuration_board,
        name="configure-board",
    ),
    # Playing
    path('game/create/', views.create_game, name="create-game"),
    path(
        'game/create/<int:game_type_id>/',
        views.create_game_redirect,
        name="create-game-redirect",
    ),
    path('game/play/<int:game_id>/', views.play_game, name="play-game"),
    path('games/', GameListView.as_view(), name="games"),
    path('users/', UserListView.as_view(), name="users"),
]

app_name = 'Chess'
