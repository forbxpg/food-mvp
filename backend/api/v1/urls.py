from django.urls import path, include

from .routers import v1_router


urlpatterns = [
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
