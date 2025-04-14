from django.urls import path, include
from rest_framework.routers import DefaultRouter


v1_router = DefaultRouter()

urlpatterns = [
    path("", include(v1_router.urls)),
]
