from django.conf import settings
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomUserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['email'] == 'mamcie@gmail.com':
            raise serializers.ValidationError({'email': 'Invalid email address.'})
        return data

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'google_password', 'profile_image', 'is_active', 'google_id', 'first_name', 'origin']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.first_name if user.origin == 'google' else user.username
        token['email'] = user.email
        token['profile_image'] = user.profile_image

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
