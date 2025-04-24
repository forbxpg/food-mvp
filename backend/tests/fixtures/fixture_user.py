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
def third_user(django_user_model):
    return django_user_model.objects.create(
        username="user3",
        email="user3@email.ru",
        password="user3password",
        first_name="User",
        last_name="Three",
    )


@pytest.fixture
def third_user_token(third_user):
    from rest_framework.authtoken.models import Token

    return {
        "auth_token": Token.objects.create(user=third_user),
    }


@pytest.fixture
def third_user_client(third_user_token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Token {third_user_token['auth_token']}",
    )
    return client


@pytest.fixture
def no_token_user(django_user_model):
    return django_user_model.objects.create_user(
        first_name="User",
        last_name="NoToken",
        username="user_no_token",
        password="user_no_token_password",
        email="absc@gmail.com",
    )


@pytest.fixture
def no_token_user_client(no_token_user):
    from rest_framework.test import APIClient

    client = APIClient()
    client.force_login(no_token_user)
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
