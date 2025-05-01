from http import HTTPStatus

import pytest

from cart.models import CartItem


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

    def test_add_recipe_to_cart_auth(self, user, user_client, recipe):
        response = user_client.post(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["id"] == recipe.id
        assert (
            CartItem.objects.filter(
                recipe=recipe,
                cart__user=user,
            ).exists()
            is True
        )

    def test_add_non_existing_recipe_to_cart(self, user_client):
        response = user_client.post(self.cart_url.format(id=9999))
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_add_recipe_to_cart_twice(self, user_client, recipe):
        response = user_client.post(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.CREATED
        assert CartItem.objects.filter(recipe=recipe).count() == 1

        response = user_client.post(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert CartItem.objects.filter(recipe=recipe).count() == 1

    def test_remove_recipe_from_cart(self, user_client, recipe):
        response = user_client.post(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.CREATED
        assert CartItem.objects.filter(recipe=recipe).count() == 1

        response = user_client.delete(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert CartItem.objects.filter(recipe=recipe).count() == 0

    def test_remove_non_existing_recipe_from_cart(self, user_client):
        response = user_client.delete(self.cart_url.format(id=9999))
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_remove_recipe_from_cart_twice(self, user_client, recipe):
        response = user_client.post(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.CREATED
        assert CartItem.objects.filter(recipe=recipe).count() == 1

        response = user_client.delete(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert CartItem.objects.filter(recipe=recipe).count() == 0

        response = user_client.delete(self.cart_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.BAD_REQUEST

    # def test_download_shopping_cart_anonymous(self, client):
    #     response = client.get(self.cart_download_url)
    #     assert response.status_code == HTTPStatus.UNAUTHORIZED
    #
    # def test_download_shopping_cart_auth(self, user_client, recipe):
    #     response = user_client.get(self.cart_download_url)
    #     assert response.status_code == HTTPStatus.OK
    #     assert (
    #         response["Content-Disposition"]
    #         == 'attachment; filename="shopping_cart.pdf"'
    #     )
