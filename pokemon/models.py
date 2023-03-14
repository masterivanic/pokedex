from django.conf import settings
from django.db import models

from pokedex.models import PokedexCreature


class Pokemon(models.Model):
    """Pokemon object"""

    pokedex_creature = models.ForeignKey(
        PokedexCreature,
        on_delete=models.CASCADE,
    )

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    nickname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    level = models.PositiveSmallIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)

    def clean(self):
        """
        Set default nickname to related pokedex creature name
        if no nickname is given
        """

        if not self.nickname:
            self.nickname = self.pokedex_creature.name
        return super().clean()

    def __str__(self):
        """
        Return Pokermon name with the trainer username if it has one

        Return Pokermon name (wild) if not
        """

        return "{} ({})".format(
            self.nickname, self.trainer.username if self.trainer else "wild"
        )

    def receive_xp(self, amount: int) -> None:
        """
        Update pokemon level based on the XP is received
        """
        self.experience += amount
        self.level = 1 + self.experience // 100
        self.save()
