from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

from recipes.models import Ingredient, Tag, Recipe, RecipeIngredient


@pytest.fixture
def ingredient():
    return Ingredient.objects.create(
        name="Test Ingredient",
        measurement_unit="kg",
    )


@pytest.fixture
def ingredient_2():
    return Ingredient.objects.create(
        name="Test Ingredient 2",
        measurement_unit="g",
    )


@pytest.fixture
def tag():
    return Tag.objects.create(
        name="Test Tag",
        slug="test-tag",
    )


@pytest.fixture
def tag_2():
    return Tag.objects.create(
        name="Test Tag 2",
        slug="test-tag-2",
    )


@pytest.fixture
def recipe(user, ingredient, tag):
    image = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"binary image data",
        content_type="image/jpeg",
    )
    recipe = Recipe.objects.create(
        author=user,
        name="Test Recipe",
        text="Test text",
        cooking_time=10,
        image=image,
    )
    recipe.tags.add(tag)
    RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        amount=10,
    )
    return recipe


@pytest.fixture
def three_recipes_from_one_user(user, ingredient, tag):
    image = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"binary image data",
        content_type="image/jpeg",
    )
    recipes = Recipe.objects.bulk_create(
        [
            Recipe(
                author=user,
                name=f"Test Recipe {i}",
                text="Test text",
                cooking_time=10,
                link=f"link{i}",
                image=image,
            )
            for i in range(1, 4)
        ]
    )
    for rec in recipes:
        rec.tags.add(tag)
        RecipeIngredient.objects.create(
            recipe=rec,
            ingredient=ingredient,
            amount=10,
        )
    return recipes


@pytest.fixture
def subscription(user, second_user):
    from users.models import Subscription

    Subscription.objects.create(
        subscribing=second_user,
        subscriber=user,
    )
