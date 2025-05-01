from http import HTTPStatus

import pytest

from favorite.models import FavoriteRecipe


@pytest.mark.django_db(transaction=True)
class TestFavoriteRecipes:
    """Тесты для модели избранных рецептов."""

    recipes_list_url = "/api/recipes/"
    recipe_detail_url = "/api/recipes/{id}/"
    favorite_url = "/api/recipes/{id}/favorite/"

    def test_add_recipe_to_favorites_anonymous(self, client, recipe):
        response = client.post(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_add_recipe_to_favorites_auth(self, user, user_client, recipe):
        response = user_client.post(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["id"] == recipe.id
        assert (
            FavoriteRecipe.objects.filter(
                recipe=recipe,
                favorite__user=user,
            ).exists()
            is True
        )

        is_favorited_response_test = user_client.get(
            self.recipe_detail_url.format(id=recipe.id),
        )
        assert is_favorited_response_test.data["is_favorited"] is True

    def test_add_non_existing_recipe_to_favorites(self, user_client):
        response = user_client.post(self.favorite_url.format(id=9999))
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_add_recipe_to_favorites_twice(self, user_client, recipe):
        response = user_client.post(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.CREATED
        assert FavoriteRecipe.objects.filter(recipe=recipe).count() == 1

        response = user_client.post(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert FavoriteRecipe.objects.filter(recipe=recipe).count() == 1

    def test_remove_recipe_from_favorites_anonymous(self, client, recipe):
        response = client.delete(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_remove_recipe_from_favorites_auth(
        self,
        user,
        user_client,
        recipe,
    ):
        response = user_client.post(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.CREATED
        assert FavoriteRecipe.objects.filter(
            recipe=recipe, favorite__user=user
        ).exists()

        response = user_client.delete(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not FavoriteRecipe.objects.filter(
            recipe=recipe, favorite__user=user
        ).exists()

    def test_remove_recipe_from_favorites_twice(self, user_client, recipe):
        response = user_client.post(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.CREATED
        assert FavoriteRecipe.objects.filter(recipe=recipe).count() == 1

        response = user_client.delete(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert FavoriteRecipe.objects.filter(recipe=recipe).count() == 0

        response = user_client.delete(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.BAD_REQUEST
