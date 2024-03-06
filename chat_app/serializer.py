from rest_framework import serializers
from .models import ChatHistory,ChatThread


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        exclude = ("archived",)

    def to_representation(self, instance: ChatHistory):
        data = super().to_representation(instance)
        data["sender"] = {
            "sender_name" : (
                                f"{instance.thread.sender.first_name} {instance.thread.sender.last_name}"
                                if instance.thread and instance.thread.sender
                                else None
                            ),
            "sender_id" : (instance.thread.sender.id if instance.thread and instance.thread.sender
                                else None)
        }

        data["receiver"] = {
            "receiver_name" : (
                                f"{instance.thread.receiver.first_name} {instance.thread.receiver.last_name}"
                                if instance.thread and instance.thread.receiver
                                else None
                            ),
            "receiver_id" : (instance.thread.receiver.id if instance.thread and instance.thread.receiver
                                else None)
        }


        return data



class ChatThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatThread
        exclude = ("archived",)

    def to_representation(self, instance: ChatThread):
        data = super().to_representation(instance)
        data["sender"] = {
            "sender_name" : (
                                f"{instance.thread.sender.first_name} {instance.thread.sender.last_name}"
                                if instance.thread and instance.thread.sender
                                else None
                            ),
            "sender_id" : (instance.thread.sender.id if instance.thread and instance.thread.sender
                                else None)
        }

        data["receiver"] = {
            "receiver_name" : (
                                f"{instance.thread.receiver.first_name} {instance.thread.receiver.last_name}"
                                if instance.thread and instance.thread.receiver
                                else None
                            ),
            "receiver_id" : (instance.thread.receiver.id if instance.thread and instance.thread.receiver
                                else None)
        }


        return data


class GetThreadIdSerializer(serializers.Serializer):
    thread_id = serializers.IntegerField(required=True)


class GetThreadByUserSerializer(serializers.Serializer):
    thread_id = serializers.IntegerField(required=True)