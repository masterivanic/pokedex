from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserCreateSerializer
from .serializers import UserSerializer

UserModel = get_user_model()


class UserViewSet(GenericViewSet):
    authentication_classes = ()
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "register":
            return UserCreateSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=("POST",),
        authentication_classes=(),
        serializer_class=UserCreateSerializer,
    )
    def register(self, request):
        """API endpoint to register as a trainer"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=("GET",), authentication_classes=(JWTAuthentication,))
    def me(self, request):
        """API endpoint to understand deeply who you are"""
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)
