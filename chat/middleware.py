from django.contrib.auth import get_user_model
from rest_framework_simplejwt.backends import TokenBackend
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from loguru import logger


@database_sync_to_async
def get_user(token, user):
    from django.contrib.auth.models import AnonymousUser

    User = get_user_model()

    try:
        valid_data = TokenBackend(algorithm="HS256").decode(token, verify=False)
        user_id = valid_data["user_id"]

        if int(user_id) != int(user):
            return None

        logger.info("here")
        user = User.objects.filter(id=user_id).first()
        logger.info(user)

        return user if user else None

    except Exception as e:
        logger.error(f"failed {e}")
        return AnonymousUser(), None


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser

        logger.info("auth")
        logger.debug(scope)

        try:

            token_key = (
                dict((x.split("=") for x in scope["query_string"].decode().split("&")))
            ).get("token", None)

            logger.info(token_key)

            user = (
                dict((x.split("=") for x in scope["query_string"].decode().split("&")))
            ).get("user", None)

            logger.info(user)

        except Exception as e:
            logger.exception(e)
            token_key = None

        scope["user"] = (
            AnonymousUser() if token_key == None else await get_user(token_key, user)
        )
        logger.debug(scope)

        return await super().__call__(scope, receive, send)
