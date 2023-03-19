from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PokemonTeamViewSet
from .views import PokemonViewSet

app_name = "pokemon"

router = DefaultRouter()
router.register(r"^pokemon-team", PokemonTeamViewSet)
router.register("", PokemonViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
