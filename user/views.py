from django.contrib.auth import login, get_user_model
from django.shortcuts import render

from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from chat.utils import CustomPagination, serializer_errors, error_400

from user.serializer import (
    UserSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    UserRegistrationSerializer,
)

from user.models import User

User = get_user_model()


class AuthViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "head", "patch"]

    @extend_schema(request=UserRegistrationSerializer)
    @action(
        detail=False,
        methods=["post"],
        authentication_classes=[],
        permission_classes=[AllowAny],
    )
    def create_user(self, request):
        user = self.request.user

        serializer = UserRegistrationSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            email = result["email"]

            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "code": status.HTTP_201_CREATED,
                    "status": "success",
                    "message": " User created successfully",
                    "data": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            default_errors = serializer.errors
            error_message = serializer_errors(default_errors)

            return Response(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "status": "error",
                    "message": error_message,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(request=LoginSerializer)
    @action(
        detail=False,
        methods=["post"],
        authentication_classes=[],
        permission_classes=[AllowAny],
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            try:
                user = User.objects.get(email=email.lower())
                refresh = RefreshToken.for_user(user)

            except:
                return error_400("User does not exist")

            if user.is_verified:
                if user.is_active:
                    if user.check_password(password):
                        the_serializer = UserSerializer
                        user_data = the_serializer(user).data
                        login(request, user)

                        response = Response(
                            {
                                "code": 200,
                                "status": "success",
                                "message": "Login Sucessful",
                                "user_info": user_data,
                                "token": {
                                    "refresh": str(refresh),
                                    "access": str(refresh.access_token),
                                },
                                "access_duration": settings.SIMPLE_JWT[
                                    "ACCESS_TOKEN_LIFETIME"
                                ],
                            },
                            status=status.HTTP_200_OK,
                        )

                        return response

                    else:
                        return error_400("Incorrect Email/Password Inserted")

                else:
                    return error_400("User is not active. Kindly contact your admin")

            else:
                return Response(
                    {
                        "code": 406,
                        "status": "failed",
                        "message": "User is not verified. Kindly contact admin",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        else:
            default_errors = serializer.errors
            error_message = serializer_errors(default_errors)
            return error_400(error_message)

    @extend_schema(request=ChangePasswordSerializer)
    @action(detail=False, methods=["put"])
    def update_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]

            if not user.check_password(old_password):
                return Response(
                    {"status": "failed", "message": "Incorrect Password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response(
                {"status": "success", "message": "Password changed successfully"},
                status=status.HTTP_200_OK,
            )

        else:
            default_errors = serializer.errors
            error_message = serializer_errors(default_errors)
            return error_400(error_message)


   

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "head", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs["pk"]

        the_user = User.objects.filter(id=pk).first()

        if the_user == user:
            return the_user


    @extend_schema(exclude=True)    
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.email = f"{instance.email}__deleted"
        instance.is_active = False
        instance._is_verified = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


def index(request):
    return render(request, 'index.html')
    