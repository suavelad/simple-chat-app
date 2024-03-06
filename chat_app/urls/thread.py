from chat_app import views as view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", view.ChatThreadViewSet, "chat_thread")

urlpatterns = router.urls
