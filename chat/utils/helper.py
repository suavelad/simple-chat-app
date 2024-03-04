from rest_framework.pagination import PageNumberPagination


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
