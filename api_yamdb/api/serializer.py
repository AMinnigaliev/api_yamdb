from rest_framework import serializers


class SignupSerializer(serializers.Seializer):
    email = serializers.EmailField(max_length=254, requared=True)
    username = serializers.CharField(max_length=150, requared=True)


class TokenSerializer(serializers.Seializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(max_length=150, requared=True)
