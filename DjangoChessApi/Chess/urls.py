from django.urls import path

from . import views


urlpatterns = [
    path('configure/', views.chess_create_configuration, name="configure"),
    path('configure/<int:game_type_id>/', views.chess_configuration, name="configure-edit")
]

app_name = 'Chess'
