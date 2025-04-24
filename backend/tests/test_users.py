import json
from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestUsersLoginLogout:
    """Класс для тестирования создания пользователей."""

    users_list_url = "/api/users/"
    users_token_login_url = "/api/auth/token/login/"
    users_token_logout_url = "/api/auth/token/logout/"
    user_password_reset_url = "/api/users/set_password/"
    test_data = {
        "email": "testmail80@gmail.com",
        "password": "testdata123",
        "first_name": "Auth",
        "last_name": "User",
        "username": "authuser",
    }

    # User create tests

    def test_user_create_with_invalid_data(self, client):
        response = client.post(
            self.users_list_url,
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_create_user_and_authorize(self, client):
        create_response = client.post(
            self.users_list_url,
            data=json.dumps(self.test_data),
            content_type="application/json",
        )
        assert create_response.status_code == HTTPStatus.CREATED
        assert create_response.data["username"] == self.test_data["username"]

        token_get_response = client.post(
            self.users_token_login_url,
            data={
                "email": self.test_data["email"],
                "password": self.test_data["password"],
            },
        )

        assert token_get_response.status_code == HTTPStatus.OK
        assert "auth_token" in token_get_response.data

    def test_auth_user_logout(self, user_client):
        response = user_client.post(self.users_token_logout_url)
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_anonymous_logout(self, client):
        response = client.post(self.users_token_logout_url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db(transaction=True)
class TestUsersUpdateDeleteList:
    """Класс для тестирования списка users и отдельных объектов user."""

    users_list_url = "/api/users/"
    users_detail_url = "/api/users/{id}/"
    current_user_detail_url = "/api/users/me/"
    user_avatar_url = "/api/users/me/avatar/"

    def test_get_user_list(self, client, four_users):
        response = client.get(self.users_list_url)
        assert response.status_code == HTTPStatus.OK
        assert len(response.data["results"]) == 4
        limit_response = client.get(self.users_list_url, {"limit": 1})
        assert limit_response.status_code == HTTPStatus.OK
        assert len(limit_response.data["results"]) == 1

    def test_get_user_detail(self, client, user):
        response = client.get(self.users_detail_url.format(id=user.id))
        assert response.status_code == HTTPStatus.OK
        assert response.data["username"] == user.username

    def test_current_user_endpoint_anonymous(self, client):
        response = client.get(self.current_user_detail_url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_current_user_endpoint_authorized(self, user_client, user):
        response = user_client.get(self.current_user_detail_url)
        assert response.status_code == HTTPStatus.OK
        assert response.data["username"] == user.username

    def test_user_avatar_update_anonymous(self, client):
        response = client.post(
            self.user_avatar_url,
            data={"image": "next will be the real avatar, yes im lazy!"},
            content_type="multipart/form-data",
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_user_avatar_update_delete_auth(self, user_client, user):
        response = user_client.put(
            self.user_avatar_url,
            data={
                "avatar": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD// \
                        /9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            },
        )
        assert response.status_code == HTTPStatus.OK
        get_avatar_response = user_client.get(self.users_detail_url.format(id=user.id))
        print(get_avatar_response.data)
        assert get_avatar_response.status_code == HTTPStatus.OK
        assert (
            get_avatar_response.data["avatar"].endswith(".jpg") is True
            or get_avatar_response.data["avatar"].endswith(".png") is True
        )
        delete_response = user_client.delete(self.user_avatar_url)
        assert delete_response.status_code == HTTPStatus.NO_CONTENT

    def test_non_existing_user_profile(self, client):
        response = client.get(self.users_detail_url.format(id=999999))
        assert response.status_code == HTTPStatus.NOT_FOUND
