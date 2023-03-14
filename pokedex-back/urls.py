from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("", lambda r: redirect("api/swagger/")),
    path("pokedex/", include("pokedex.urls")),
]

if "pokemon" in settings.INSTALLED_APPS:
    urlpatterns.append(path("pokemon/", include("pokemon.urls")))

if "authentication" in settings.INSTALLED_APPS:
    urlpatterns.append(path("", include("authentication.urls")))
