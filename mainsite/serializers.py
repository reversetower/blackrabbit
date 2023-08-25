#serializers.py
from .models import TrcTech
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class TrcTechSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrcTech
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "groups"]
        extra_kwargs = {"password": {"write_only": True}, "groups": {"read_only": True}}


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"