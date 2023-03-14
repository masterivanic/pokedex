from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import PokedexCreatureFilter
from .models import PokedexCreature
from .serializers import PokedexCreatureDetailSerializer
from .serializers import PokedexCreatureSerializer


class PokedexViewSet(ReadOnlyModelViewSet):
    """API endpoint to display all Pokedex Creatures"""

    permission_classes = (AllowAny,)
    authentication_classes = ()
    queryset = PokedexCreature.objects.all().order_by("ref_number")
    serializer_class = PokedexCreatureSerializer
    filterset_class = PokedexCreatureFilter

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":
            return PokedexCreatureDetailSerializer

        return self.serializer_class
