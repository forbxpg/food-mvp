from django.urls import path, include

from .views import download_cart_api_view
from .routers import v1_router


urlpatterns = [
    path("recipes/download_shopping_cart/", download_cart_api_view),
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
