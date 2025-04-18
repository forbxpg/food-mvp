from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from api.v1.views.recipe import RetrieveRecipeViaShortLinkView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("<slug:short_link>/", RetrieveRecipeViaShortLinkView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
