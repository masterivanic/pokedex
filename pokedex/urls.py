from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PokedexViewSet

app_name = "pokedex"

router = DefaultRouter()
router.register("", PokedexViewSet, basename="pokedex")


urlpatterns = [
    path("", include(router.urls)),
]
