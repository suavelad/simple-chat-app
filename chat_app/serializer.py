from rest_framework import serializers
from .models import ChatHistory


class ChatHistorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        exclude = ("archived",)

    def to_representation(self, instance: ChatHistory):
        data = super().to_representation(instance)
        data["name"] = (
            f"{instance.user.first_name} {instance.user.last_name}"
            if instance.user
            else None
        )

        return data
