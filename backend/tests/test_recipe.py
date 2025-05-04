import json
from http import HTTPStatus

import pytest

from recipes.models import Recipe


@pytest.mark.django_db(transaction=True)
class TestRecipesListCreate:

    recipe_list_url = "/api/recipes/"
    recipe_detail_url = "/api/recipes/{id}/"

    # Recipe list tests
    def test_recipes_list_auth(
        self,
        user_client,
        user,
        three_recipes_from_one_user,
    ):
        """Тестирование списка рецептов для авторизованного пользователя."""
        response = user_client.get(self.recipe_list_url)
        assert response.status_code == HTTPStatus.OK
        recipes_count = Recipe.objects.count()
        assert recipes_count == 3
        assert response.data["count"] == 3
        for rec in response.data["results"]:
            assert rec["author"]["id"] == user.id

    def test_recipes_list_anonymous(
        self,
        client,
        user,
        three_recipes_from_one_user,
    ):
        """Тестирование списка рецептов для анонима."""
        response = client.get(self.recipe_list_url)
        assert response.status_code == HTTPStatus.OK
        recipes_count = Recipe.objects.count()
        assert recipes_count == 3
        assert response.data["count"] == 3
        for rec in response.data["results"]:
            assert rec["author"]["id"] == user.id

    def test_recipes_list_with_limit_param(
        self,
        client,
        user,
        three_recipes_from_one_user,
    ):
        """Проверка доступности списка рецептов с параметром limit."""
        response = client.get(self.recipe_list_url, {"limit": 1})
        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 3
        assert len(response.data["results"]) == 1

    def test_recipes_list_with_author_param(
        self,
        user,
        client,
        three_recipes_from_one_user,
    ):
        """Проверка доступности списка рецептов с параметром author."""
        response = client.get(self.recipe_list_url, {"author": user.id})
        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 3
        for rec in response.data["results"]:
            assert rec["author"]["id"] == user.id

    # Recipe detail tests
    def test_recipe_detail_anonymous(
        self,
        client,
        recipe,
    ):
        """Проверка доступности детальной информации
        о рецепте для анонимного пользователя.
        """
        response = client.get(self.recipe_detail_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.OK
        assert response.data["id"] == recipe.id

    def test_recipe_detail_auth(
        self,
        user_client,
        recipe,
    ):
        """Проверка доступности детальной информации
        о рецепте для авторизованного пользователя.
        """
        response = user_client.get(
            self.recipe_detail_url.format(id=recipe.id),
        )
        assert response.status_code == HTTPStatus.OK
        assert response.data["id"] == recipe.id

    # Recipe creation tests
    def test_recipe_create_no_auth(self, client):
        """Проверка создания рецепта без авторизации."""
        response = client.post(self.recipe_list_url, data={})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_recipe_create_with_invalid_data(self, user_client, user):
        response = user_client.post(self.recipe_list_url, data={})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_recipe_create_with_valid_data(
        self,
        user_client,
        tag,
        ingredient_2,
    ):
        data = {
            "name": "Test Recipe",
            "text": "Test text",
            "cooking_time": 10,
            "tags": [tag.id],
            "ingredients": [
                {
                    "id": ingredient_2.id,
                    "amount": 2,
                },
            ],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA \
AEAAAABAgMAAABieywaAAAACVBMVEUAAAD// \
/9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACkl \
EQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
        }
        response = user_client.post(
            self.recipe_list_url,
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.CREATED
        recipes_count = Recipe.objects.count()
        assert recipes_count == 1

    def test_recipe_create_with_no_image(self, user_client):
        """Проверка создания рецепта без изображения."""
        data = {
            "name": "Test Recipe",
            "text": "Test text",
            "cooking_time": 10,
            "tags": [1],
            "ingredients": [
                {
                    "id": 1,
                    "amount": 2,
                },
            ],
        }
        response = user_client.post(
            self.recipe_list_url,
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db(transaction=True)
class TestRecipeUpdateDelete:
    """Тестирование обновления и удаления рецептов."""

    recipe_list_url = "/api/recipes/"
    recipe_detail_url = "/api/recipes/{id}/"

    # Recipe update tests
    def test_recipe_update_no_auth(self, client, recipe):
        """Проверка обновления рецепта без авторизации."""
        response = client.patch(
            self.recipe_detail_url.format(id=recipe.id),
            data={},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_recipe_update_not_author(
        self,
        recipe,
        second_user_client,
        second_user,
    ):
        """Проверка обновления рецепта не автором."""
        response = second_user_client.patch(
            self.recipe_detail_url.format(id=recipe.id),
            data={"text": "Updated text"},
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_recipe_update_with_invalid_data(
        self,
        recipe,
        user_client,
    ):
        """Проверка обновления рецепта с невалидными данными."""
        response = user_client.patch(
            self.recipe_detail_url.format(id=recipe.id),
            data={},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_recipe_update_with_valid_data_author(
        self,
        user_client,
        recipe,
        tag_2,
        ingredient_2,
    ):
        """Проверка обновления рецепта с валидными данными."""
        data = {
            "name": "Updated Recipe",
            "text": "Updated text",
            "cooking_time": 20,
            "tags": [tag_2.id],
            "ingredients": [
                {
                    "id": ingredient_2.id,
                    "amount": 3,
                },
            ],
        }
        response = user_client.patch(
            self.recipe_detail_url.format(id=recipe.id),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.OK
        recipe.refresh_from_db()
        assert response.data["id"] == recipe.id

    def test_recipe_update_with_invalid_ingredient(
        self,
        user_client,
        recipe,
        tag_2,
    ):
        """Проверка обновления рецепта с невалидным ингредиентом."""
        data = {
            "name": "Updated Recipe 2",
            "text": "Updated text 2",
            "cooking_time": 22,
            "tags": [tag_2.id],
            "ingredients": [
                {
                    "id": 99999,
                    "amount": 3,
                },
            ],
        }
        response = user_client.patch(
            self.recipe_detail_url.format(id=recipe.id),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_recipe_update_with_invalid_tag(
        self,
        user_client,
        recipe,
        ingredient_2,
    ):
        """Проверка обновления рецепта с невалидным тегом."""
        data = {
            "name": "Updated Recipe 3",
            "text": "Updated text 3",
            "cooking_time": 25,
            "tags": [99999],
            "ingredients": [
                {
                    "id": ingredient_2.id,
                    "amount": 3,
                },
            ],
        }
        response = user_client.patch(
            self.recipe_detail_url.format(id=recipe.id),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_recipe_update_with_empty_ingredient(
        self,
        user_client,
        recipe,
        tag_2,
    ):
        """Проверка обновления рецепта с пустым ингредиентом."""
        data = {
            "name": "Updated Recipe 4",
            "text": "Updated text 4",
            "cooking_time": 25,
            "tags": [tag_2.id],
            "ingredients": [],
        }
        response = user_client.patch(
            self.recipe_detail_url.format(id=recipe.id),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_recipe_update_with_empty_tag(
        self,
        user_client,
        recipe,
        ingredient_2,
    ):
        """Проверка обновления рецепта с пустым тегом."""
        data = {
            "name": "Updated Recipe 5",
            "text": "Updated text 5",
            "cooking_time": 25,
            "tags": [],
            "ingredients": [
                {
                    "id": ingredient_2.id,
                    "amount": 3,
                },
            ],
        }
        response = user_client.patch(
            self.recipe_detail_url.format(id=recipe.id),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_update_non_existing_recipe(self, user_client):
        """Проверка обновления несуществующего рецепта."""
        data = {
            "name": "Updated Recipe",
            "text": "Updated text",
            "cooking_time": 20,
            "tags": [1],
            "ingredients": [
                {
                    "id": 1,
                    "amount": 3,
                },
            ],
        }
        response = user_client.patch(
            self.recipe_detail_url.format(id=99999),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    # Recipe delete tests
    def test_recipe_delete_anonymous(self, client, recipe):
        """Проверка удаления рецепта анонимом."""
        response = client.delete(self.recipe_detail_url.format(id=recipe.id))
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_recipe_delete_not_author(self, second_user_client, recipe):
        """Проверка удаления рецепта не автором."""
        response = second_user_client.delete(
            self.recipe_detail_url.format(id=recipe.id),
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_recipe_delete_author(
        self,
        user_client,
        recipe,
    ):
        """Проверка удаления рецепта автором."""
        response = user_client.delete(
            self.recipe_detail_url.format(id=recipe.id),
        )
        assert response.status_code == HTTPStatus.NO_CONTENT
        recipes_count = Recipe.objects.count()
        assert recipes_count == 0

    def test_delete_non_existing_recipe(self, user_client):
        """Проверка удаления несуществующего рецепта."""
        response = user_client.delete(
            self.recipe_detail_url.format(id=99999),
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
