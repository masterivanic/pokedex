from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PokemonViewSet

app_name = "pokemon"

router = DefaultRouter()
router.register("", PokemonViewSet, basename="pokemon")


urlpatterns = [
    path("", include(router.urls)),
]
