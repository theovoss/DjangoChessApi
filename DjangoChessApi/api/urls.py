from django.conf.urls import include, url
from django.conf import settings

from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Root

root = routers.DefaultRouter()


# App: Chess

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
