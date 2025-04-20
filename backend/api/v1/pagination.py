"""Модуль классов пагинации."""

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

from core import config


class BaseLimitOffsetPagination(LimitOffsetPagination):
    """Базовый класс пагинации для API."""

    default_limit = config.DEFAULT_PAGE_SIZE


class BasePageNumberPagination(PageNumberPagination):
    """Базовый класс пагинации для API."""

    max_page_size = config.MAX_PAGE_SIZE
    page_size = config.DEFAULT_PAGE_SIZE
    page_query_param = config.PAGE_QUERY_PARAM
    page_size_query_param = config.PAGE_SIZE_QUERY_PARAM
