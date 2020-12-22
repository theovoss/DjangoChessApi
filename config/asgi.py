import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dropdjango.settings")
django.setup()
application = get_default_application()

# import os
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import DjangoChessApi.Chess.routing
# import django


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
# django.setup()

# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             DjangoChessApi.Chess.routing.websocket_urlpatterns
#         )
#     ),
#     "http": get_asgi_application(),
# })
