from django.contrib.auth import get_user_model
from rest_framework import serializers


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer about a user"""

    class Meta:
        model = UserModel
        fields = ["id", "username", "email"]
        read_only_fields = ["id"]


class UserCreateSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)
