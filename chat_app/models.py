from django.db import models
from user.models import User


# Create your models here.
class ChatHistory(models.Model):
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
    message = models.TextField(null=True)
    archived = models.DateTimeField(blank=True, null=True, editable=False)
    is_edited = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat History ID: {self.id} | Receiver: {self.receiver.first_name} {self.receiver.last_name} | Receiver: {self.sender.first_name} {self.sender.last_name}  "
