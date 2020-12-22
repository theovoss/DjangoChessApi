import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from DjangoChessApi.Chess.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
