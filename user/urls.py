from django.urls import path, include
from user import views as view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("users", view.UserViewSet, "users")
router.register("auth", view.AuthViewSet, "auth")

urlpatterns = router.urls
