"""Модуль классов пагинации."""

from core import config
from rest_framework.pagination import PageNumberPagination


class BasePageNumberPagination(PageNumberPagination):
    """Базовый класс пагинации для API."""

    max_page_size = config.MAX_PAGE_SIZE
    page_size = config.DEFAULT_PAGE_SIZE
    page_query_param = config.PAGE_QUERY_PARAM
    page_size_query_param = config.PAGE_SIZE_QUERY_PARAM
