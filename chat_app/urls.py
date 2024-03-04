from django.urls import path, include
from chat_app import views as view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("", view.ChatHistoryViewSet, "chat_history")


urlpatterns = router.urls
