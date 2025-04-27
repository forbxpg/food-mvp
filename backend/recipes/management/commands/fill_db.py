from django.core.management.base import BaseCommand

from core.config import FIXTURE_PATH
from recipes.models import Ingredient


def get_data(filename):
    """Читает данные из json файла и возвращает список словарей."""
    import json

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError("Ошибка декодирования JSON", e)


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Команда для заполнения базы данных данными из json файла."""
        ingredients = get_data(f"{FIXTURE_PATH}/ingredients.json")
        for ingredient in ingredients:
            Ingredient.objects.get_or_create(
                name=ingredient["name"],
                measurement_unit=ingredient["measurement_unit"],
            )
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены в базу данных"))
        self.stdout.write(self.style.SUCCESS("Команда завершена"))
