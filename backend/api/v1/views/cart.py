# from http.client import HTTPResponse
#
#
# def download_cart_view(request):
#     """Метод для получения списка покупок."""
#     user = request.user
#     recipes_in_cart = Cart.objects.filter(user=user).values_list("recipe", flat=True)
#     recipes = Recipe.objects.filter(id__in=recipes_in_cart)
#     shopping_list = {}
#     for recipe in recipes:
#         ingredients = recipe.ingredients.all()
#         for ingredient in ingredients:
#             if ingredient.name not in shopping_list:
#                 shopping_list[ingredient.name] = {
#                     "measurement_unit": ingredient.measurement_unit,
#                     "amount": ingredient.amount,
#                 }
#             else:
#                 shopping_list[ingredient.name]["amount"] += ingredient.amount
#     response = HTTPResponse(content_type="text/plain")
#     response["Content-Disposition"] = 'attachment; filename="shopping_list.txt"'
#     response.write("Список покупок:\n")
#     for ingredient, data in shopping_list.items():
#         response.write(f"{ingredient}: {data['amount']} {data['measurement_unit']}\n")
#     return response
