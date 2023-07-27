from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class WatchlistPagination(PageNumberPagination):
    page_size = 10
    # page_query_param = "p" # query params for page ?p=1,2,3...
    page_size_query_param = "size"  # size of the page ?size=10
    max_page_size = 10  # max page size can be pass as query params
    last_page_strings = "end"  # last by default


class ReviewListPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10
    limit_query_param = "limit"  # default
    offset_query_param = "start"  # default offset
