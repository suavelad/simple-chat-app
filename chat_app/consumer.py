import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

from chat_app.models import ChatHistory,ChatThread
from loguru import logger

from user.models import User



@database_sync_to_async
def save_chat_history(receive_data,receiver_user_id, user):
    # from user.models import User

    message = receive_data.get("message", None)
    chat_id = receive_data.get("chat_id", None)

    receiver_user = User.objects.filter(id=receiver_user_id).first()
    sender_user = user


    if receiver_user and sender_user:

        chat_thread,_ = ChatThread.objects.get_or_create(sender=sender_user,receiver=receiver_user)
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
                "thread_id": history.thread.id,
                "sender": history.sender.username,
                "timestamp": str(history.date_created),
            }
        else:
            return None
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
def get_thread_id(sender_user,receiver_user_id):
    # from user.models import User
     
    receiver_user = User.objects.filter(id=receiver_user_id).first()
    if not receiver_user:
        return None
    
    chat_thread,_ = ChatThread.objects.get_or_create(sender=sender_user,receiver=receiver_user)
    return chat_thread.id


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.info("Connecting......")

        user = self.scope.get("user")

        if isinstance(user, AnonymousUser):
            logger.error("Annon")
            pass

        if user and user.is_authenticated:
            receiver_user_id = self.scope['url_route']['kwargs']['receiver_id']

            thread_id = await get_thread_id(user,receiver_user_id)

            self.group_name = f'thread_{thread_id}'
            await self.channel_layer.group_add(self.group_name,self.channel_name)
            
            await self.accept()
            logger.info("Connected....")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):

        receive_data = json.loads(text_data)
        user = self.scope.get("user")
        receiver_user_id = self.scope['url_route']['kwargs']['receiver_id']
        if user.is_authenticated:

            payload = await save_chat_history(receive_data,receiver_user_id, user)
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


class ChatReadStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.info("Connecting......")

        user = self.scope.get("user")

        if isinstance(user, AnonymousUser):
            logger.error("Annon")
            pass

        if user and user.is_authenticated:
            
            self.group_name = 'receipt'
            await self.channel_layer.group_add(self.group_name,self.channel_name)

            await self.accept()
            logger.info("Connected....")

    async def disconnect(self, close_code):
        pass

    async def send_read_receipt(self, event):
            data = json.loads(event.get('value'))
            receiver_id = data['receiver_id']
            read_status = data['status']
            thread_id = data['thread_id']
            await self.send(text_data=json.dumps({
                'receiver_id':receiver_id,
                'thread_id': thread_id,
                'read_status':read_status
            }))


    async def receive(self, text_data=None, bytes_data=None):

        receive_data = json.loads(text_data)
        user = self.scope.get("user")
        if user.is_authenticated:
            await update_chat_read_status(receive_data)

        else:
            logger.debug("Not authenticated")
            response_data = {"message": "User is not authenticated", "data": []}
            await self.send(text_data=json.dumps(response_data))