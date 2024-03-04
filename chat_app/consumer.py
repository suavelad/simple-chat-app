import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

from chat_app.models import ChatHistory
from loguru import logger


@database_sync_to_async
def save_chat_history(receive_data, user):
    from user.models import User

    sender = receive_data.get("sender", None)
    receiver = receive_data.get("receiver", None)
    message = receive_data.get("message", None)
    chat_id = receive_data.get("chat_id", None)

    receiver_user = User.objects.filter(id=receiver).first()
    sender_user = User.objects.filter(id=sender).first()

    if receiver_user and (receiver_user == user) and sender_user:
        history = (
            ChatHistory()
            if chat_id == None
            else ChatHistory.objects.filter(id=int(chat_id)).first()
        )
        history.sender = sender_user
        history.receiver = receiver_user
        history.message = message
        history.save()

        return {
            "type": "chat.message",
            "content": message,
            "sender": history.sender.username,
            "timestamp": str(history.date_created),
        }
    else:
        return None


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.info("Connecting......")

        user = self.scope.get("user")

        if isinstance(user, AnonymousUser):
            logger.error("Annon")
            pass

        if user and user.is_authenticated:
            self.group_name = user.username
            await self.channel_layer.group_add(self.group_name, self.channel_name)

            await self.accept()
            logger.info("Connected....")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):

        receive_data = json.loads(text_data)
        user = self.scope.get("user")
        if user.is_authenticated:
            payload = await save_chat_history(receive_data, user)
            if payload:
                await self.send(text_data=json.dumps(payload))

            else:
                logger.debug("Not authenticated")
                response_data = {"message": "User is not authenticated", "data": []}
                await self.send(text_data=json.dumps(response_data))

        else:
            logger.debug("Not authenticated")
            response_data = {"message": "User is not authenticated", "data": []}
            await self.send(text_data=json.dumps(response_data))
