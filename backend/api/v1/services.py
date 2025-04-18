from uuid import uuid4

from django.conf import settings

from core.config import SHORT_LINK_LENGTH


def generate_short_link():
    """Генерирует короткий слаг для рецепта."""
    short_link = str(uuid4())[:SHORT_LINK_LENGTH]
    return short_link, f"{settings.SITE_URL}/{short_link}"
