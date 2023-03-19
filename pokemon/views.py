from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import PokemonFilter
from .models import Pokemon
from .models import PokemonTeam
from .models import TeamID
from .serializers import PokemonDetailsSerializer
from .serializers import PokemonGiveXPSerializer
from .serializers import PokemonSerializer
from .serializers import PokemonTeamAssignSerializer
from .serializers import PokemonTeamIDSerializer
from .serializers import PokemonTeamMessageSerializer
from .serializers import PokemonTeamSerializer
from .serializers import PokemonTeamsInfoSerializer
from .serializers import PokemonTeamUpdateSerializer
from pokemon_object.models import get_random_object


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

    def get_queryset(self):
        """get pokemon's user who is authenticated"""
        return self.queryset.filter(trainer=self.request.user)

    def create(self, request, *args, **kwargs):
        """create user while making a request and set random pokemon object"""
        data = request.data
        data["pokemon_object"] = get_random_object().pk
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@extend_schema_view(
    create=extend_schema(description="API endpoint to create a pokemon team\n\n"),
    list=extend_schema(
        description="API endpoint to get a pokemon team list of a connected trainer"
    ),
    retrieve=extend_schema(
        description="API endpoint pokemon team, which gives on us detailed informations"
    ),
    update=extend_schema(description="API endpoint to modify pokemon team's name"),
    destroy=extend_schema(
        description="API endpoint to delete a pokemon team without deleting pokemon member team"
    ),
)
class PokemonTeamViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = PokemonTeam.objects.all()
    serializer_class = PokemonTeamSerializer

    def get_serializer_class(self):
        if self.action == "get_team_ids":
            return PokemonTeamIDSerializer
        elif self.action == "get_teams_info":
            return PokemonTeamsInfoSerializer
        elif self.action == "update":
            return PokemonTeamUpdateSerializer
        elif self.action == "remove_pokemon_from_team":
            return PokemonTeamMessageSerializer
        elif self.action == "assign_pokemon_team":
            return PokemonTeamAssignSerializer

        return PokemonTeamSerializer

    def get_queryset(self):
        """get pokemon's team of user"""
        return self.queryset.filter(trainer=self.request.user)

    def check_pokemon_team(self, id_team) -> bool:
        """check if a team is own by a trainer"""
        team_trainer_list = self.get_queryset()
        pokemon_team = get_object_or_404(PokemonTeam, pk=id_team)
        if pokemon_team in team_trainer_list:
            return True
        return False

    @action(methods=["GET"], detail=False, url_path="get-team-ids")
    def get_team_ids(self, request):
        """get team's trainer ids"""
        teams_ids = [TeamID(team.pk) for team in self.get_queryset()]
        serializer = self.get_serializer(teams_ids, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=["GET"], detail=False, url_path=r"get-teams-info/(?P<id_team>[\d-]+)"
    )
    def get_teams_info(self, request, id_team: int):
        """get team and pokemon of team"""
        pokemon_team = get_object_or_404(PokemonTeam, pk=id_team)
        if pokemon_team:
            pokemon_list = Pokemon.objects.filter(
                trainer=request.user.id, pokemon_team=pokemon_team
            )
            context = {
                "name": pokemon_team.name,
                "pokemons": [
                    PokemonSerializer(instance=pokemon).data
                    for pokemon in pokemon_list
                    if pokemon_list
                ],
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        """create a trainer team"""
        data = request.data
        data["trainer"] = request.user.pk
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        """update a trainer team name"""
        try:
            pokemon_team = get_object_or_404(self.get_queryset(), pk=pk)
            pokemon_team.name = request.data["name"]
            pokemon_team.save()
            context = {"id": pk, "name": pokemon_team.name}
            return Response(context, status=status.HTTP_200_OK)
        except PokemonTeam.DoesNotExist as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["PUT"],
        detail=False,
        url_path=r"assign-pokemon-team/(?P<id_team>[\d-]+)/(?P<id_pokemon>[\d-]+)",
    )
    def assign_pokemon_team(self, request, id_team, id_pokemon):
        """assign a pokemon team of a train"""
        pokemon = get_object_or_404(Pokemon, pk=id_pokemon)
        pokemon_team = get_object_or_404(PokemonTeam, pk=id_team)
        team_trainer_list = self.get_queryset()
        trainer_pokemon_list = Pokemon.objects.filter(trainer=request.user.id)

        if pokemon in trainer_pokemon_list:
            if pokemon_team in team_trainer_list:
                pokemon.pokemon_team_id = pokemon_team.id
                pokemon.save()
                context = {
                    "pokemon_id": pokemon.id,
                    "pokemon_team": pokemon.pokemon_team.name,
                }
                return Response(context, status=status.HTTP_200_OK)
        return Response(
            {"message": "pokemon id or pokemon team is invalid"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=["PUT"],
        detail=False,
        url_path=r"remove-pokemon-from-team/(?P<id_team>[\d-]+)/(?P<id_pokemon>[\d-]+)",
    )
    def remove_pokemon_from_team(self, request, id_team, id_pokemon):
        """remove a pokemon from a trainer team"""
        trainer_pokemon_list = Pokemon.objects.filter(trainer=request.user.id)
        pokemon_team = get_object_or_404(PokemonTeam, pk=id_team)
        pokemon = get_object_or_404(Pokemon, pk=id_pokemon)
        is_my_team = self.check_pokemon_team(id_team=id_team)
        try:
            if pokemon in trainer_pokemon_list:
                if is_my_team:
                    if pokemon.pokemon_team.name == pokemon_team.name:
                        pokemon.pokemon_team_id = None
                        pokemon.save()
                        return Response(
                            {"message": "Pokemon remove successfully"},
                            status=status.HTTP_200_OK,
                        )
                return Response(
                    {"message": "Pokemon or pokemon team is invalid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_404_NOT_FOUND)
