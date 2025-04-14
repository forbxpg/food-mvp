from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .routers import v1_router


urlpatterns = [
    path("", include(v1_router.urls)),
]
