from .models import PokemonPreferredObject
from .serializers import PokemonPreferredObjectSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.

class PokemonPreferredObjectViewSet(ModelViewSet):
    
    permission_classes = (AllowAny,)
    queryset = PokemonPreferredObject.objects.all()
    serializer_class = PokemonPreferredObjectSerializer
    http_method_names = ['get', 'delete']

    @action(methods=['get'], detail=False, url_path='get_pokemon_object_by_name/(?P<name>\w+)')
    def get_pokemon_object_by_name(self, request, name):
        query = get_object_or_404(PokemonPreferredObject, name = name)
        serializer = self.serializer_class(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

