from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import ChatHistory, ChatThread
from .serializer import (
    ChatHistorySerializer,
    ChatThreadSerializer,
    GetThreadIdSerializer,
    GetThreadByUserSerializer,
)
from chat.utils import CustomPagination, serializer_errors, error_400

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action


# Create your views here.
class ChatHistoryViewSet(ModelViewSet):
    queryset = ChatHistory.objects.all().order_by("-id")
    serializer_class = ChatHistorySerializer
    pagination_class = CustomPagination
    http_method_names = ["get", "head", "delete"]

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs["pk"]

        chat_history = ChatHistory.objects.filter(id=pk).first()

        if chat_history.sender == user or chat_history.receiver == user:
            return chat_history

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(parameters=[GetThreadIdSerializer])
    @action(
        detail=False,
        methods=["get"],
    )
    def get_chat_by_thread_id(self, request):

        serializer = GetThreadIdSerializer(data=self.request.query_params)

        if serializer.is_valid(raise_exception=True):
            thread_id = serializer.data.get("thread_id")
            chats = ChatHistory.objects.filter(thread_id=thread_id)

            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "message": "successful",
                    "data": ChatHistorySerializer(chats, many=True).data,
                },
                status=status.HTTP_200_OK,
            )

        else:
            default_errors = serializer.errors
            error_message = serializer_errors(default_errors)
            return error_400(error_message)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.archive()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatThreadViewSet(ModelViewSet):
    queryset = ChatThread.objects.all().order_by("-id")
    serializer_class = ChatThreadSerializer
    pagination_class = CustomPagination
    http_method_names = ["get", "head", "delete"]

    @extend_schema(parameters=[GetThreadByUserSerializer])
    @action(
        detail=False,
        methods=["get"],
    )
    def get_thread_by_user(self, request):
        serializer = GetThreadByUserSerializer(data=self.request.query_params)

        if serializer.is_valid(raise_exception=True):
            user_id = serializer.data.get("user_id")
            threads = ChatThread.objects.filter(
                Q(receiver_id=user_id) | Q(sender_id=user_id)
            )

            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "message": "successful",
                    "data": ChatThreadSerializer(threads, many=True).data,
                },
                status=status.HTTP_200_OK,
            )

        else:
            default_errors = serializer.errors
            error_message = serializer_errors(default_errors)
            return error_400(error_message)
