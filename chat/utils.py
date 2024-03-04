from rest_framework.pagination import PageNumberPagination
from loguru import logger

from rest_framework import status, serializers
from rest_framework.response import Response
from django.http import JsonResponse


page_size_query_param = "limit"
page_query_param = "offset"


class CustomPagination(PageNumberPagination):
    page_size_query_param = page_size_query_param
    page_query_param = page_query_param

    def get_paginated_response(self, data):
        return {
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "results": data,
        }


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
