import random

from django.db import models


def get_random_object():
    list_object = PokemonPreferredObject.objects.all()
    if list_object:
        rand_index = random.randint(0, len(list_object))
        return list_object[rand_index]
    return None


class PokemonPreferredObject(models.Model):
    """Pokemon Preferred object's"""

    name = models.CharField(max_length=100, blank=True, null=False)
    image = models.CharField(max_length=200, blank=True, null=False)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Pokemon Preferred object's"

    def __str__(self) -> str:
        return self.name
