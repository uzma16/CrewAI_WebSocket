# import os

# # Update the below import lib
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from api.routing import websocket_urlpatterns
# from api.middleware import TokenAuthMiddleware


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
# # 👇 2. Update the application var
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AllowedHostsOriginValidator(
#         TokenAuthMiddleware(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         ),
#     )
# })

# app = application

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

import django
django.setup()  # Explicitly setup Django to load apps

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from api.routing import websocket_urlpatterns
from api.middleware import TokenAuthMiddleware

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
    )
})

