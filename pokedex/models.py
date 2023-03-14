from django.db import models


class PokedexCreature(models.Model):
    """PokedexCreature object"""

    name = models.CharField(max_length=100, unique=True)
    ref_number = (
        models.PositiveSmallIntegerField()
    )  # Many creature can have same ref_number

    generation = models.PositiveSmallIntegerField()
    legendary = models.BooleanField(default=False)

    type_1 = models.CharField(max_length=20)
    type_2 = models.CharField(max_length=20, blank=True, null=True)
    total = models.PositiveSmallIntegerField()

    hp = models.PositiveSmallIntegerField()
    attack = models.PositiveSmallIntegerField()
    defense = models.PositiveSmallIntegerField()
    special_attack = models.PositiveSmallIntegerField()
    special_defence = models.PositiveSmallIntegerField()
    speed = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """Return creature name"""
        return self.name
