from rest_framework import serializers
from .models import PokemonPreferredObject


class PokemonPreferredObjectSerializer(serializers.ModelSerializer):
    """Serializer of Pokemon's object preferred """
    class Meta:
        model = PokemonPreferredObject
        fields = (
            "id",
            "name",
            "image",
            "description"
        )
        read_only_fields = ("id",)