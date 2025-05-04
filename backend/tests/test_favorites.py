from http import HTTPStatus

import pytest

from favorite.models import Favorite


@pytest.mark.django_db(transaction=True)
class TestFavoriteRecipes:
    """Тесты для модели избранных рецептов."""

    recipes_list_url = "/api/recipes/"
    recipe_detail_url = "/api/recipes/{id}/"
    favorite_url = "/api/recipes/{id}/favorite/"

    def test_add_recipe_to_favorites_anonymous(self, client, recipe):
        response = client.post(self.favorite_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.UNAUTHORIZED
