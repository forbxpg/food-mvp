from http import HTTPStatus

import pytest
from cart.models import Cart


@pytest.mark.django_db(transaction=True)
class TestCartItems:
    """Тесты для модели корзины."""

    recipes_list_url = "/api/recipes/"
    recipe_detail_url = "/api/recipes/{id}/"
    cart_url = "/api/recipes/{id}/shopping_cart/"
    cart_download_url = "/api/recipes/download_shopping_cart/"

    def test_add_recipe_to_cart_anonymous(self, client, recipe):
        response = client.post(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_add_recipe_to_cart_authenticated(
        self,
        user_client,
        recipe,
        user,
    ):
        response = user_client.post(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.CREATED
        assert Cart.objects.filter(user=user, recipe=recipe).exists()
        assert response.data == {
            "id": recipe.id,
            "name": recipe.name,
            "image": recipe.image.url,
            "cooking_time": recipe.cooking_time,
        }
