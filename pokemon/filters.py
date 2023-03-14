from django_filters import rest_framework as filters

from .models import Pokemon


class PokemonFilter(filters.FilterSet):
    """Filters for pokedex creature listing"""

    nickname = filters.CharFilter(field_name="nickname", lookup_expr="icontains")
    wild = filters.BooleanFilter(field_name="trainer_id", lookup_expr="isnull")
    name = filters.CharFilter(
        field_name="pokedex_creature__name", lookup_expr="icontains"
    )
    type_1 = filters.CharFilter(
        field_name="pokedex_creature__type_1", lookup_expr="icontains"
    )
    type_2 = filters.CharFilter(
        field_name="pokedex_creature__type_2", lookup_expr="icontains"
    )
    generation = filters.NumberFilter(field_name="pokedex_creature__generation")
    legendary = filters.BooleanFilter(field_name="pokedex_creature__legendary")

    class Meta:
        model = Pokemon
        fields = [
            "trainer",
            "nickname",
            "pokedex_creature",
        ]
