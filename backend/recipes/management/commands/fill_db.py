"""Команда для заполнения базы данных данными из json файла."""

from django.core.management.base import BaseCommand
from django.db import transaction

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
        ingredients_data = get_data(f"{FIXTURE_PATH}/ingredients.json")
        try:
            with transaction.atomic():
                Ingredient.objects.bulk_create(
                    [
                        Ingredient(
                            name=ingredient["name"],
                            measurement_unit=ingredient["measurement_unit"],
                        )
                        for ingredient in ingredients_data
                    ],
                    ignore_conflicts=True,
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
            self.stdout.write(
                self.style.ERROR("Не удалось загрузить данные в базу данных")
            )
            return
        self.stdout.write(
            self.style.SUCCESS("Данные успешно загружены в базу данных"),
        )
        self.stdout.write(self.style.SUCCESS("Команда завершена"))
