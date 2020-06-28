from rest_framework.pagination import PageNumberPagination


class BackendPagination(PageNumberPagination):
    page_size_query_param = 'count'
    max_page_size = 50
