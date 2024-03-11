import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ChatHistory

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=ChatHistory)
def send_read_receipt(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()

        data = {
            "receiver_id": instance.thread.receiver.id,
            "status": instance.read_receipt,
            "thread_id": instance.thread.id,
            "chat_id": instance.id,
        }
        group_name = f"receipt_{instance.thread.id}"

        async_to_sync(channel_layer.group_send)(
            group_name, {"type": "send_read_receipt", "value": json.dumps(data)}
        )


@receiver(post_save, sender=ChatHistory)
def send_message_to_receiver(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        data = {"chat_id": instance.id}
        group_name = f"thread_user_{instance.receiver.id}"

        async_to_sync(channel_layer.group_send)(
            group_name, {"type": "send_to_receiver", "value": json.dumps(data)}
        )
