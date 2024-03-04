from django.conf import settings
from decouple import config

REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_PASSWORD = config("REDIS_PASSWORD")
REDIS_USERNAME = config("REDIS_USERNAME")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}")
            ],
        },
    },
}
