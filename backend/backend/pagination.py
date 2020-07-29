from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
import math


class BackendPagination(PageNumberPagination):
    page_size_query_param = 'count'
    page_size = 10
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'meta': OrderedDict([
                ('current_page', self.page.number),
                ('all_pages', math.ceil(self.page.paginator.count/self.page_size)),
                ('count_on_page', self.page_size),
                ('total', self.page.paginator.count),
            ]),
            'results': data,
        })
