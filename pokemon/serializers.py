from rest_framework import serializers

from authentication.serializers import UserSerializer
from pokedex.serializers import PokedexCreatureDetailSerializer
from pokemon.models import Pokemon
from pokemon.models import PokemonTeam


class PokemonSerializer(serializers.ModelSerializer):
    """Serializer of Pokemon object"""

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "pokedex_creature",
            "trainer",
            "nickname",
            "level",
            "experience",
            "pokemon_object",
        )
        read_only_fields = ("id", "level")

    def validate(self, attrs):
        """Add pokemon nickname if no nickname is given"""
        nickname = attrs.get("nickname")
        pokedex_creature = attrs.get("pokedex_creature")
        if not nickname:
            attrs["nickname"] = pokedex_creature.name

        return super().validate(attrs)


class PokemonDetailsSerializer(serializers.ModelSerializer):
    pokedex_creature = PokedexCreatureDetailSerializer()
    trainer = UserSerializer()

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "nickname",
            "level",
            "experience",
            "pokedex_creature",
            "trainer",
        )


class PokemonGiveXPSerializer(serializers.Serializer):
    """Serializer of give-xp endpoint"""

    amount = serializers.IntegerField(min_value=0)


class PokemonTeamSerializer(serializers.ModelSerializer):
    """Serializer of Pokemon team"""

    class Meta:
        model = PokemonTeam
        fields = ("id", "name", "trainer")
        read_only_fields = ("id",)


class PokemonTeamIDSerializer(serializers.Serializer):
    team_id = serializers.IntegerField(min_value=0)


class PokemonTeamsInfoSerializer(serializers.ModelSerializer):
    """Serializer of Pokemon team"""

    pokemon = PokemonSerializer()

    class Meta:
        model = PokemonTeam
        fields = (
            "name",
            "pokemon",
        )


class PokemonTeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonTeam
        fields = (
            "id",
            "name",
        )


class PokemonTeamMessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class PokemonTeamAssignSerializer(serializers.Serializer):
    pokemon_id = serializers.IntegerField(min_value=0)
    pokemon_team = serializers.CharField()
