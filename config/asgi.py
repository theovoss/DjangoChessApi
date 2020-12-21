import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
import DjangoChessApi.Chess.routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

django.setup()
application = get_default_application()


# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             DjangoChessApi.Chess.routing.websocket_urlpatterns
#         )
#     ),
#     "http": get_asgi_application(),
# })
