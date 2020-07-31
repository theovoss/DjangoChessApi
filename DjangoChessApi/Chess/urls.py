from django.urls import path

from . import views


urlpatterns = [
    path('', views.chess_configuration),
]

app_name = 'Chess'
