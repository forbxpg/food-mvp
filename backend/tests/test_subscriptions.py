from http import HTTPStatus

import pytest
from users.models import Subscription


@pytest.mark.django_db(transaction=True)
class TestSubscriptions:
    """Класс для тестирования подписок."""

    subscriptions_list_url = "/api/users/subscriptions/"
    subscribe_url = "/api/users/{id}/subscribe/"
    user_detail_url = "/api/users/{id}/"

    def test_get_subscriptions_list_anonymous(self, client):
        """Проверка получения списка подписок анонимным пользователем."""
        response = client.get(self.subscriptions_list_url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_get_subscriptions_list_auth(
        self,
        user,
        user_client,
        subscription,
        second_user,
    ):
        response = user_client.get(self.subscriptions_list_url)
        assert response.status_code == HTTPStatus.OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == second_user.id

    def test_create_subscription_obj(self, user, second_user):
        """Создание подписки на объект."""
        subs = Subscription.objects.create(
            subscribing=user,
            subscriber=second_user,
        )
        assert subs.subscriber == second_user
        assert subs.subscribing == user
        assert subs.id is not None

    def test_create_subsctiption_anonymous(self, client, user, user_client):
        """Создание подписки анонимным пользователем."""
        response = client.post(self.subscribe_url.format(id=user.id), data={})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_create_subscription_auth(
        self,
        second_user_client,
        user,
        second_user,
    ):
        """Создание подписки для тестов."""
        response = second_user_client.post(
            self.subscribe_url.format(id=user.id),
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["id"] == user.id
        assert (
            Subscription.objects.filter(
                subscribing=user,
                subscriber=second_user,
            ).exists()
            is True
        )

    def test_create_subscription_twice(
        self, user_client, subscription, user, second_user
    ):
        response = user_client.post(
            self.subscribe_url.format(id=user.id),
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            Subscription.objects.filter(
                subscribing=second_user, subscriber=user
            ).count()
            == 1
        )

    def test_create_self_subscription(
        self,
        user_client,
        user,
    ):
        """Создание подписки на себя."""
        response = user_client.post(
            self.subscribe_url.format(id=user.id),
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            Subscription.objects.filter(
                subscribing=user,
                subscriber=user,
            ).exists()
            is False
        )

    def test_delete_subscription_anonymous(self, client, user):
        response = client.delete(
            self.subscribe_url.format(id=user.id),
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_delete_subscription_auth(
        self,
        user_client,
        second_user,
        second_user_client,
        user,
    ):
        subscription_response = user_client.post(
            self.subscribe_url.format(id=second_user.id),
            data={},
        )
        assert subscription_response.status_code == HTTPStatus.CREATED
        assert subscription_response.data["id"] == second_user.id
        assert (
            Subscription.objects.filter(
                subscribing=second_user,
                subscriber=user,
            ).exists()
            is True
        )

        subscription_list_response = user_client.get(
            self.subscriptions_list_url,
        )
        data = subscription_list_response.data["results"][0]["id"]
        assert subscription_list_response.status_code == HTTPStatus.OK
        assert len(subscription_list_response.data["results"]) == 1
        assert data == second_user.id

        delete_response = user_client.delete(
            self.subscribe_url.format(id=second_user.id),
        )
        assert delete_response.status_code == HTTPStatus.NO_CONTENT
        assert (
            Subscription.objects.filter(
                subscribing=second_user,
                subscriber=user,
            ).exists()
            is False
        )
        subscriptions_list_response = user_client.get(
            self.subscriptions_list_url,
        )
        assert subscriptions_list_response.status_code == HTTPStatus.OK
        assert len(subscriptions_list_response.data["results"]) == 0

    def test_delete_subscription_twice(
        self,
        user_client,
        subscription,
        user,
        second_user,
    ):
        response = user_client.delete(
            self.subscribe_url.format(id=second_user.id),
        )
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert (
            Subscription.objects.filter(
                subscribing=second_user,
                subscriber=user,
            ).exists()
            is False
        )
