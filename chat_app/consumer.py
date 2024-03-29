import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

from chat_app.models import ChatHistory, ChatThread
from loguru import logger

from user.models import User


@database_sync_to_async
def save_chat_history(receive_data, user):

    message = receive_data.get("message", None)
    chat_id = receive_data.get("chat_id", None)
    receiver_user_id = receive_data.get("receiver_id", None)

    receiver_user = User.objects.filter(id=receiver_user_id).first()
    sender_user = user

    if receiver_user and sender_user:

        chat_thread, _ = ChatThread.objects.get_or_create(
            sender=sender_user, receiver=receiver_user
        )
        history = (
            ChatHistory()
            if chat_id == None
            else ChatHistory.objects.filter(id=int(chat_id)).first()
        )
        if history:
            history.sender = user
            history.receiver = receiver_user
            history.message = message
            history.thread = chat_thread

            if chat_id:
                history.is_edited = True
            history.save()

            return {
                "type": "chat.message",
                "content": message,
                "chat_id": history.id,
                "thread_id": history.thread.id,
                "sender": {
                    "sender": f"{history.sender.first_name} {history.sender.last_name}",
                    "sender_id": history.sender.id,
                },
                "receiver": {
                    "receiver": f"{history.receiver.first_name} {history.receiver.last_name}",
                    "receiver_id": history.receiver.id,
                },
                "timestamp": str(history.date_created),
            }
        else:
            return None
    else:
        return None


@database_sync_to_async
def forward_to_receiver(chat_id):

    chat_history = ChatHistory.objects.filter(id=int(chat_id)).first()

    if chat_history:
        chat_history.read_receipt = True
        chat_history.read_timestamp = datetime.now()
        chat_history.save()
        return {
            "type": "chat.message",
            "content": chat_history.message,
            "chat_id": chat_history.id,
            "thread_id": chat_history.thread.id,
            "sender": {
                "sender": f"{chat_history.thread.sender.first_name} {chat_history.thread.sender.last_name}",
                "sender_id": chat_history.thread.sender.id,
            },
            "receiver": {
                "receiver": f"{chat_history.thread.receiver.first_name} {chat_history.thread.receiver.last_name}",
                "receiver_id": chat_history.thread.receiver.id,
            },
            "timestamp": str(chat_history.date_created),
        }

    else:
        return None


@database_sync_to_async
def update_chat_read_status(receive_data):

    status = receive_data.get("status", None)
    chat_id = receive_data.get("chat_id", None)

    if chat_id:
        history = ChatHistory.objects.filter(id=int(chat_id)).first()
        if history:
            history.read_receipt = True if status.capitalize() else False
            history.read_timestamp = datetime.now()
            history.save()

        else:
            return None
    else:
        return None


@database_sync_to_async
def get_thread_id(sender_user=None, receiver_user_id=None, thread_id=None):
    if thread_id:
        chat_thread = ChatThread.objects.filter(id=thread_id).first()
        return chat_thread.id

    receiver_user = User.objects.filter(id=receiver_user_id).first()

    if not receiver_user:
        return None

    chat_thread, _ = ChatThread.objects.get_or_create(
        sender=sender_user, receiver=receiver_user
    )
    return chat_thread.id


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.info("Connecting......")

        user = self.scope.get("user")

        if isinstance(user, AnonymousUser):
            logger.error("Annon")
            logger.debug("Not authenticated")
            return

        if user and user.is_authenticated:

            self.group_name = f"thread_user_{user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)

            await self.accept()
            logger.info("Connected....")

    async def disconnect(self, close_code):
        pass

    async def send_to_receiver(self, event):
        data = json.loads(event.get("value"))
        chat_id = data["chat_id"]
        payload = await forward_to_receiver(chat_id)
        if payload:
            await self.send(text_data=json.dumps(payload))

    async def receive(self, text_data=None, bytes_data=None):

        receive_data = json.loads(text_data)
        user = self.scope.get("user")
        if user.is_authenticated:

            payload = await save_chat_history(receive_data, user)
            if payload:
                response_data = {
                    "message": "Message Sent",
                    "timestamp": str(datetime.now()),
                }
                await self.send(text_data=json.dumps(response_data))

                # await self.send(text_data=json.dumps(payload))

            else:
                logger.debug("Not authenticated")
                response_data = {"message": "User is not authenticated", "data": []}
                await self.send(text_data=json.dumps(response_data))

        else:
            logger.debug("Not authenticated")
            response_data = {"message": "User is not authenticated", "data": []}
            await self.send(text_data=json.dumps(response_data))


class ChatReadStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.info("Connecting......")

        user = self.scope.get("user")

        if isinstance(user, AnonymousUser):
            logger.error("Annon")
            pass

        if user and user.is_authenticated:

            self.group_name = f"thread_user_{user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)

            await self.accept()
            logger.info("Connected....")

    async def disconnect(self, close_code):
        pass

    async def send_read_receipt(self, event):
        data = json.loads(event.get("value"))
        receiver_id = data["receiver_id"]
        read_status = data["status"]
        thread_id = data["thread_id"]
        chat_id = data["chat_id"]
        await self.send(
            text_data=json.dumps(
                {
                    "receiver_id": receiver_id,
                    "thread_id": thread_id,
                    "read_status": read_status,
                    "chat_id": chat_id,
                }
            )
        )

    async def receive(self, text_data=None, bytes_data=None):

        receive_data = json.loads(text_data)
        user = self.scope.get("user")
        if user.is_authenticated:
            await update_chat_read_status(receive_data)

        else:
            logger.debug("Not authenticated")
            response_data = {"message": "User is not authenticated", "data": []}
            await self.send(text_data=json.dumps(response_data))
