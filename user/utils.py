import jwt
import pyotp
import base64
import jwt

from django.contrib.auth import get_user_model

from datetime import datetime

from django.conf import settings
from rest_framework_jwt.settings import api_settings

User = get_user_model()


class generateKey:
    @staticmethod
    def returnValue(email):
        return f"{email}{datetime.date(datetime.now())}{settings.SECRET_KEY}"


def generate_otp(contact, verification=False):
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(contact).encode())

    if verification == True:
        hotp = pyotp.HOTP(key)
        user = User.objects.filter(Q(email=contact) | Q(phone=contact)).first()
        otp_data = hotp.at(int(user.id))
        return otp_data

    OTP = pyotp.TOTP(key, interval=settings.PASSWORD_OTP_TIMEOUT)
    otp_data = OTP.now()

    return otp_data
