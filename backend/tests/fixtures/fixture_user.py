import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        username="user1",
        email="user1@email.ru",
        password="user1password",
        first_name="User",
        last_name="One",
    )


@pytest.fixture
def first_user_token(user):
    from rest_framework.authtoken.models import Token

    return {
        "auth_token": Token.objects.create(user=user),
    }


@pytest.fixture()
def user_client(first_user_token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Token {first_user_token['auth_token']}",
    )
    return client


@pytest.fixture
def second_user(django_user_model):
    return django_user_model.objects.create(
        username="user2",
        email="user2@email.ru",
        password="forxbpgdata2",
        first_name="User",
        last_name="Two",
    )


@pytest.fixture
def second_user_token(second_user):
    from rest_framework.authtoken.models import Token

    return {
        "auth_token": Token.objects.create(user=second_user),
    }


@pytest.fixture
def second_user_client(second_user_token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Token {second_user_token['auth_token']}",
    )
    return client


@pytest.fixture
def four_users():
    from django.contrib.auth import get_user_model

    User = get_user_model()

    User.objects.bulk_create(
        [
            User(
                username=f"usertest{i}",
                email=f"avds{i}lol{i+1}@s.ru",
                password=f"testingpwd{i}",
                first_name="User{i}",
                last_name="Test{i}",
            )
            for i in range(1, 5)
        ]
    )
