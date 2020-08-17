from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('configure/', views.create_configuration, name="configure"),
    path('configure/<int:game_type_id>/', views.configuration, name="configure-edit"),
    path(
        'configure/<int:game_type_id>/board',
        views.configuration_board,
        name="configure-board",
    ),
    path('game/create/', views.create_game, name="create-game"),
    path(
        'game/create/<int:game_type_id>/',
        views.create_game_redirect,
        name="create-game-redirect",
    ),
    path('game/play/<int:game_id>/', views.play_game, name="play-game"),
]

app_name = 'Chess'
