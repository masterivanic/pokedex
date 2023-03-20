from django.contrib import admin

from pokemon.models import Pokemon
from pokemon.models import PokemonTeam


class PokemonInline(admin.StackedInline):
    model = Pokemon


class PokemonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pokemon._meta.fields]
    ordering = ("pokedex_creature__ref_number",)
    search_fields = ("nickname", "trainer__username")
    readonly_fields = ("pokemon_object",)
    list_per_page = 50

    autocomplete_fields = ("pokedex_creature", "trainer")


class PokemonTeamAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "number_of_pokemon",
    )
    list_filter = ("name",)
    search_fields = ("name__startswith", "trainer__username")
    list_per_page = 50

    inlines = [PokemonInline]

    def number_of_pokemon(self, obj):
        num_pokemon = Pokemon.objects.filter(pokemon_team=obj).count()
        return num_pokemon


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonTeam, PokemonTeamAdmin)

admin.site.site_header = "POKEDEX Admin"
admin.site.site_title = "POKEDEX Admin Portal"
admin.site.index_title = "Welcome to POKEDEX Portal"
