from django.contrib import admin

from pokemon_object.models import PokemonPreferredObject


class PokemonPreferredObjectAdmin(admin.ModelAdmin):
    list_display = ("name", "image")
    list_per_page = 50


admin.site.register(PokemonPreferredObject, PokemonPreferredObjectAdmin)
