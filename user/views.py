from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializer import CustomUserSerializer
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from .serializer import CustomUserSerializer
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect
from .serializer import MyTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.http import Http404
from django.db.models import Q
from operator import __or__ as OR
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import parse_id_token
from django.forms.models import model_to_dict


@csrf_exempt
def google_login_view(request):

    id_token = json.loads(request.body.decode('utf-8')).get('tokenId')
    data = parse_id_token(id_token)
    if not data:
        return JsonResponse({'status': 'false', 'message': 'Invalid id token'}, status=401)
    try:
        user = CustomUser.objects.get(google_id=data.get('sub'))
        access_token = MyTokenObtainPairSerializer(data={'username': user.username, 'password': user.google_password})
        if access_token.is_valid():
            return JsonResponse({'ownAccessToken': access_token.validated_data['access']}, safe=False)
        else:
            return JsonResponse({'status': 'false', 'message': 'Invalid token'}, status=401)

    except CustomUser.DoesNotExist:
        password = CustomUser.objects.make_random_password()
        data = {
            'first_name': data.get('name'),
            'email': data.get('email'),
            'profile_image': data.get('picture'),
            'google_id': data.get('sub'),
            'date_joined': datetime.now(),
            'username': data.get('email'),
            'origin': 'google',
            'google_password': password
        }

        valid_user = CustomUserSerializer(data=data)

        if valid_user.is_valid():
            user = valid_user.save()
            access_token = MyTokenObtainPairSerializer(data={'username': user.username, 'password': user.google_password})
            if access_token.is_valid():
                return JsonResponse({'ownAccessToken': access_token.validated_data['access'], 'new_user': True}, safe=False)

        return JsonResponse({'status': 'false', 'message': valid_user.errors}, status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
def sing_up_view(request):
    new_user = CustomUser(email=request.data.get('email', None),
                          username=request.data.get('username', None),
                          origin='own',
                          date_joined=datetime.now())

    data = {
        'email': request.data.get('email', None),
        'date_joined': datetime.now(),
        'username': request.data.get('username', None),
        'origin': 'own'
    }

    valid_user = CustomUserSerializer(data=model_to_dict(new_user))

    if valid_user.is_valid():
        new_user.set_password(request.data.get('password', None))
        new_user.save()
        return Response({'message': 'Successfully create account.'})
    errors = {key: value[0] for key, value in valid_user.errors.items()}
    return Response({'status': 'false', 'errors': errors}, status=401)
