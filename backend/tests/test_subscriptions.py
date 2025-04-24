from http import HTTPStatus

import pytest

from users.models import Subscription


@pytest.mark.django_db(transaction=True)
class TestSubscriptions:
	"""Класс для тестирования подписок."""

	subscriptions_list_url = "/api/users/subscriptions/"

	def test_get_subscriptions_list_anonymous(self, client):
		"""Проверка получения списка подписок анонимным пользователем."""
		response = client.get(self.subscriptions_list_url)
		assert response.status_code == HTTPStatus.UNAUTHORIZED

