from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from api.v1.views import GetRecipeViaLinkAPIView


urlpatterns = [
    path("f/<slug:short_link>", GetRecipeViaLinkAPIView.as_view()),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
