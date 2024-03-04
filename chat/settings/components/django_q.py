from decouple import config


REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_PASSWORD = config("REDIS_PASSWORD")
REDIS_USERNAME = config("REDIS_USERNAME")

REDIS_URL = f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": REDIS_URL,
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "CLIENT_CLASS": "",
            # "CONNECTION_POOL_KWARGS": {"ssl_cert_reqs": None},
            "PASSWORD": REDIS_PASSWORD,
        },
    }
}


Q_CLUSTER = {
    "timeout": 300,
    "retry": 350,
    "workers": 4,
    "django_redis": "default",
    "max_attempts": 1,
}
