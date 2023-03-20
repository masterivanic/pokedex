from django.contrib import admin
from django.utils.html import mark_safe

from pokemon_object.models import PokemonPreferredObject


class PokemonPreferredObjectAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "image_view")
    list_per_page = 50
    readonly_fields = ["image_view"]

    def image_view(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image,
                width=50,
                height=50,
            )
        )


admin.site.register(PokemonPreferredObject, PokemonPreferredObjectAdmin)
