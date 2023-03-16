from django.contrib import admin
from .models import PokemonPreferredObject

# Register your models here.
class PokemonPreferredObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    list_per_page = 50

admin.site.register(PokemonPreferredObject, PokemonPreferredObjectAdmin)

"""
 create a interface admin
 to enable and disable and api
 
"""