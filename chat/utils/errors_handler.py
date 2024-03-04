from loguru import logger
from rest_framework.response import Response
from rest_framework import status


def serializer_errors(default_errors):
    logger.debug("Errors:", default_errors)
    error_messages = ""
    for field_name, field_errors in default_errors.items():
        if field_errors[0].code == "unique":
            error_messages += f"{field_name} already exists, "
        else:
            error_messages += f"{field_name} is {field_errors[0].code}, "
    return error_messages


def error_400(message):
    return Response(
        {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "error",
            "message": message,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )
