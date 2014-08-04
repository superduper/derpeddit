from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SingUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError("Username has been already taken")
        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "id")