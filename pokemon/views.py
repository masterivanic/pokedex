from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import PokemonFilter
from .models import Pokemon
from .serializers import PokemonDetailsSerializer
from .serializers import PokemonGiveXPSerializer
from .serializers import PokemonSerializer


@extend_schema_view(
    create=extend_schema(
        description="API endpoint to create a pokemon\n\nSome fields are optionnal : trainer, nickname, level, experience"
    ),
    list=extend_schema(
        description="API endpoint to get a list of pokemons, with filtering options"
    ),
    retrieve=extend_schema(
        description="API endpoint to retrieve a specific pokemon, which gives on him detailed informations"
    ),
    update=extend_schema(description="API endpoint to modify a specific pokemon"),
    partial_update=extend_schema(
        description="API endpoint to partially modify a specific pokemon\n\nAll fields are optionnal"
    ),
    destroy=extend_schema(
        description="API endpoint to delete a specific pokemon. It's horrible"
    ),
)
class PokemonViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Pokemon.objects.all().order_by("pokedex_creature__ref_number")
    serializer_class = PokemonSerializer
    filterset_class = PokemonFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PokemonDetailsSerializer
        elif self.action == "give_xp":
            return PokemonGiveXPSerializer

        return PokemonSerializer

    @action(methods=["POST"], detail=True, url_path="give_xp")
    @extend_schema(responses=PokemonSerializer)
    def give_xp(self, request, pk=None):
        """Action to give extra experience points to a pokemon"""
        pokemon: Pokemon = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pokemon.receive_xp(serializer.validated_data["amount"])
        pokemon.save()

        response_serializer = PokemonSerializer(instance=pokemon)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
