from django.conf import settings
from django.conf.urls import include, url

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from .viewsets.game_configuration import (
    CaptureActionViewSet,
    DirectionViewSet,
    GameTypeViewSet,
    MovementViewSet,
    StandardChessPiecesViewSet,
)
from .viewsets.game_play import MoveViewSet
from .viewsets.history import HistoryViewSet


# Root

root = routers.DefaultRouter()


# App: Chess
# TODO: scope api's under /configure and /play
root.register(r'movements', MovementViewSet, basename="movements")
root.register(r'directions', DirectionViewSet, basename="directions")
root.register(r'capture-actions', CaptureActionViewSet, basename="capture-actions")
root.register(r'standard-chess', StandardChessPiecesViewSet, basename="standard-chess")
root.register(r'chess-configuration', GameTypeViewSet, basename="chess-configuration")
root.register(r'move', MoveViewSet, basename="move")
root.register(r'history', HistoryViewSet, basename="history")

# root.register(...)


# URLs
schema_view = get_schema_view(
    openapi.Info(
        title="DjangoChessApi",
        default_version='0',
        description="The API for DjangoChessApi.",
    ),
    url=settings.BASE_URL,
)

urlpatterns = [
    url('^', include(root.urls)),
    url('^client/', include('rest_framework.urls')),
    url('^docs/', schema_view.with_ui('swagger')),
]
