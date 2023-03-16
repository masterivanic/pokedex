from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PokemonPreferredObjectViewSet

app_name = "pokemon_object"

router = DefaultRouter()
router.register("", PokemonPreferredObjectViewSet, basename="pokemon_object")


urlpatterns = [
    path("", include(router.urls)),
]
