import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import PokemonPreferredObject


class Command(BaseCommand):
    """
    Create PokemonPreferredObject instances from CSV file
    """

    help = "Import list_objets_pokemon CSV file and create PokemonPreferredObject instances"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file_path",
            type=str,
            nargs="?",
            default=os.path.join(settings.BASE_DIR, "liste_objets_pokemon.csv"),
        )

    def handle(self, *args, **options):
        count = 0
        csv_file_path = options.get("csv_file_path", None)
        if csv_file_path and csv_file_path.endswith(".csv"):
            with open(csv_file_path, encoding="utf8", errors='ignore') as csvfile:
                reader = csv.reader(csvfile)
             
                for row in reader:
                    if count == 0:
                        noms_list = ";".join(row).split(";")
                        noms_list.remove('nom')
                    elif count == 1:
                        image_list = ";".join(row).split(";")
                        image_list.remove('image')
                    elif count == 2:
                        description_list = ";".join(row).split(";")
                        description_list.remove('description')
                        description_list = description_list[0:343]

                    count += 1

                pokemon_objects = [
                    PokemonPreferredObject(
                        name=element,
                        image=image_list[i],
                        description=description_list[i],
                    )
                    for i, element in enumerate(noms_list)
                ]

                PokemonPreferredObject.objects.bulk_create(
                    pokemon_objects,
                    batch_size=100,
                    # ignore_conflicts=True,
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Nb of pokemon object imported to the database: "
                        f"{len(pokemon_objects)}."
                    )
                )
        else:
            self.stderr.write(self.style.ERROR("This is not a CSV file."))
