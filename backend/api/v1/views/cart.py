"""Модуль представлений для работы со списком покупок."""

from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from api.v1.services import get_recipes_for_txt_file


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def download_cart_api_view(request):
    """Представление для скачивания списка покупок."""
    content = get_recipes_for_txt_file(request.user.cart)
    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = 'attachment; filename="list"'
    return response
