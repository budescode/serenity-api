from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
    )


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 300000000

class PostNumberPagination(PageNumberPagination):
    page_size = 0


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100000000000000000000000000000000000000000000
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 1000