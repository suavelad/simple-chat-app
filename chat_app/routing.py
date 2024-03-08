from django.urls import re_path
from .consumer import ChatConsumer, ChatReadStatusConsumer

websocket_urlpatterns = [
    re_path(r"^ws/chat/(?P<receiver_id>\d+)/$", ChatConsumer.as_asgi()),
    re_path(
        r"^ws/chat/read_status/(?P<thread_id>\d+)/$", ChatReadStatusConsumer.as_asgi()
    ),
]
