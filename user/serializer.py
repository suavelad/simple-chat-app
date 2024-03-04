import time
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "is_active",
            "is_verified",
            "is_staff",
            "password",
            "is_superuser",
            "user_permissions",
            "groups",
            "username",
        )


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    gender = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")

        password = validated_data.pop("password")
        email = validated_data["email"]
        first_name = validated_data["first_name"]

        ut = str(time.time())

        username = f"{first_name}_{ut}"

        username = username.strip("").replace(" ", "_").lower()

        existing_user = User.objects.filter(email=email).first()

        if not existing_user:
            new_user = User.objects.create(**validated_data)
            new_user.set_password(password)
            new_user.is_verified = True
            new_user.is_active = True
            new_user.username = username
            new_user.save()

            return validated_data

        else:
            raise serializers.ValidationError(
                {"code": 400, "status": "error", "message": "User already exist"}
            )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class OTPVerificationSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True)
    user_verify = serializers.BooleanField(required=False)


class EmailandPhoneNumberSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(choices=["email", "sms"], required=True)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)


class SendOTPSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(choices=["email", "sms"], required=True)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    has_partnership = serializers.BooleanField(required=False)


class ConfirmResetTokenSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)
