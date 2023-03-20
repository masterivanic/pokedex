from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import Pokemon
from .models import PokemonTeam
from .models import TeamID
from .serializers import PokemonSerializer
from .serializers import PokemonTeamIDSerializer
from pokemon.IPokemon import IPokemonTeam


class PokemonTeamService(IPokemonTeam):
    QUERYSET = None

    def set_queryset(self, query):
        self.QUERYSET = query

    def check_pokemon_team(self, id_team) -> bool:
        """check if a team is own by a trainer"""
        pokemon_team = get_object_or_404(PokemonTeam, pk=id_team)
        if pokemon_team in self.QUERYSET:
            return True
        return False

    def get_team_id(self):
        teams_ids = [TeamID(team.pk) for team in self.QUERYSET]
        serializer = PokemonTeamIDSerializer(teams_ids, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def get_teams_info(self, user, id_team: int):
        pokemon_team = get_object_or_404(PokemonTeam, pk=id_team)
        if pokemon_team:
            pokemon_list = Pokemon.objects.filter(
                trainer=user.id, pokemon_team=pokemon_team
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

    def assign_pokemon_team(self, user, id_team, id_pokemon):
        pokemon = get_object_or_404(Pokemon, pk=id_pokemon)
        pokemon_team = get_object_or_404(PokemonTeam, pk=id_team)
        trainer_pokemon_list = Pokemon.objects.filter(trainer=user.id)

        if pokemon in trainer_pokemon_list:
            if pokemon_team in self.QUERYSET:
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

    def remove_pokemon_from_team(self, user, id_team, id_pokemon):
        trainer_pokemon_list = Pokemon.objects.filter(trainer=user.id)
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
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class Context:
    strategy: IPokemonTeam

    def __init__(self, strategy: IPokemonTeam) -> None:
        self.strategy = strategy
