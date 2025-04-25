"""Утилиты API."""

import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ImageField


class Base64Field(ImageField):
    def to_internal_value(self, data):
        """Метод для преобразования данных аватара в Base64."""

        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"avatar.{ext}")
        return super().to_internal_value(data)
