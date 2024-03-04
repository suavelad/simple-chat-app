"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")

import django

django.setup()

from chat.middleware import TokenAuthMiddleware

from chat_app.routing import websocket_urlpatterns


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": OriginValidator(
            TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
            ["*"],
        ),
    }
)
