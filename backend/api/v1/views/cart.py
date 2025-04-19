from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def download_cart_api_view(request):
    """Представление для скачивания списка покупок."""
    cart_items = request.user.cart.cart_items.all()
    content = "Список покупок: \n\n"
    for index, item in enumerate(cart_items):
        recipe = item.recipe
        content += f"Recipe {index} {recipe.name}:\n "
        content += f"Ingredients:\n"
        for ingredient in recipe.ingredients.all():
            content += (
                f"- {ingredient.name}: {ingredient} {ingredient.measurement_unit}\n"
            )
        content += "\n"
    content += "End of shopping list.\n"

    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = 'attachment; filename="shopping_list.pdf"'
    return response
