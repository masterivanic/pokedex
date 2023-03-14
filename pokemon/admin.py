from django.contrib import admin

from pokemon.models import PokedexCreature
from pokemon.models import Pokemon


class PokemonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pokemon._meta.fields if field.name != "id"]
    ordering = ("pokedex_creature__ref_number",)
    search_fields = ("nickname", "trainer__username")
    list_per_page = 50

    autocomplete_fields = ("pokedex_creature", "trainer")


admin.site.register(Pokemon, PokemonAdmin)
