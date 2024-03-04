from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import ChatHistory
from .serializer import ChatHistorysSerializer
from chat.utils import CustomPagination


# Create your views here.
class ChatHistoryViewSet(ModelViewSet):
    queryset = ChatHistory.objects.all().order_by("-id")
    serializer_class = ChatHistorysSerializer
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "head", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs["pk"]

        chat_history = ChatHistory.objects.filter(id=pk).first()

        if chat_history.sender == user or chat_history.receiver == user:
            return chat_history

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.archive()
        return Response(status=status.HTTP_204_NO_CONTENT)
