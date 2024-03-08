from django.db import models
from user.models import User


# Create your models here.


class ChatThread(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="user_sender",
        null=True,
        blank=True,
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="user_receipient",
        null=True,
        blank=True,
    )
    archived = models.DateTimeField(blank=True, null=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Thread ID: {self.id} "


class ChatHistory(models.Model):
    thread = models.ForeignKey(
        ChatThread,
        on_delete=models.SET_NULL,
        related_name="chat_thread",
        null=True,
        blank=True,
    )
    message = models.TextField(null=True)
    archived = models.DateTimeField(blank=True, null=True, editable=False)
    is_edited = models.BooleanField(default=False)
    read_receipt = models.BooleanField(default=False)
    read_timestamp = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat History ID: {self.id} | Receiver: {self.thread.receiver.first_name} {self.thread.receiver.last_name} | Receiver: {self.thread.sender.first_name} {self.thread.sender.last_name}  "
