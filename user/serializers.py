from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from .models import ClientUser, User


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise AuthenticationFailed('Invalid username or password')
        return {'user': user}

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return token.key


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password1 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = ClientUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'password',
            'password1',
            'email',
            'phone_number',
        )

    def create(self, validated_data):
        password = validated_data['password']
        password1 = validated_data['password1']
        if password != password1:
            raise serializers.ValidationError({"password": "The two password fields must match."})
        user = ClientUser.objects.create_user(
            username=validated_data['username'],
            password=password,
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number']
        )
        return user