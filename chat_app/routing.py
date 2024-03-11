from django.urls import re_path
from .consumer import ChatConsumer, ChatReadStatusConsumer

websocket_urlpatterns = [
    re_path(r"^ws/chat/$", ChatConsumer.as_asgi()),
    re_path(r"^ws/chat/read_status/$", ChatReadStatusConsumer.as_asgi()),
]
