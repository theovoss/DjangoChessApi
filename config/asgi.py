import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import DjangoChessApi.Chess.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            DjangoChessApi.Chess.routing.websocket_urlpatterns
        )
    ),
    "http": get_asgi_application(),
})
