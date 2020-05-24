from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import MovieSerializer
from .models import Movie
from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny
import random 
import pandas as pd
import numpy as np

@api_view(['POST'])
def add_movie(request):
    data = request.data
    user = request.user

    try:
        Movie.objects.get(user=user, movie_id=data['movie_id'])
        return Response({'status': 'false', 'message': "The movie has already added."}, status=401)

    except Movie.DoesNotExist:
        new_movie = Movie(user=user, movie_id=data['movie_id'])
        new_movie.save()
        pagination = Paginator(Movie.objects.filter(user=user).order_by('-date_add'), data['pagination'])

        if data['withFill']:
            fill_video = pagination.page(data['current_page']).object_list[0]

            print(pagination.num_pages)
            return Response({'new_movie': MovieSerializer(fill_video).data, 'total_page': pagination.num_pages})
        else:

            return Response({'new_movie': MovieSerializer(new_movie).data, 'total_page': pagination.num_pages})


@api_view(['POST'])
def remove_movie(request):
    data = request.data
    user = request.user

    try:

        Movie.objects.get(user=user, movie_id=data['movie_id']).delete()
        order = 'date_add' if data['order'] == 'oldest' else '-date_add'

        pagination = Paginator(Movie.objects.filter(user=user).order_by(order), data['pagination'])

        if data['withFill']:

            fill_video = pagination.page(data['current_page']).object_list[data['pagination']-1]
            print(pagination.num_pages)

            return Response({'fill_movie': MovieSerializer(fill_video).data, 'total_page': pagination.num_pages})
        else:

            return Response({'message': 'Successfully has removed movie.', 'total_page': pagination.num_pages})

    except Movie.DoesNotExist:
        return Response({'status': 'false', 'message': "Movie does not exist.."}, status=401)

@api_view(['POST'])
def add_to_favourite(request):
    data = request.data
    user = request.user
    try:
        movie = Movie.objects.get(user=user, movie_id=data['movie_id'])
        movie.favourite = True
        movie.save()
        return Response({'message': 'Successfully add movie to favourite.'})
    except Movie.DoesNotExist:
        return Response({'status': 'false', 'message': "Movie does not exist.."}, status=401)


@api_view(['POST'])
def remove_from_favourite(request):
    data = request.data
    user = request.user

    try:

        movie = Movie.objects.get(user=user, movie_id=data['movie_id'])
        movie.favourite = False
        movie.save()
        order = 'date_add' if data['order'] == 'oldest' else '-date_add'


        if data['favourite']:
            print(data['favourite'])
            print(Movie.objects.filter(user=user, favourite=data['favourite']).order_by(order))
            pagination = Paginator(Movie.objects.filter(user=user, favourite=data['favourite']).order_by(order), data['pagination'])
        else:
            pagination = Paginator(Movie.objects.filter(user=user).order_by(order), data['pagination'])

        if data['withFill']:

            fill_video = pagination.page(data['current_page']).object_list[data['pagination']-1]
            print(fill_video)

            return Response({'fill_movie': MovieSerializer(fill_video).data, 'total_page': pagination.num_pages})
        else:

            return Response({'message': 'Successfully has removed movie.', 'total_page': pagination.num_pages})

    except Movie.DoesNotExist:
        return Response({'status': 'false', 'message': "Movie does not exist.."}, status=401)


@api_view(['GET'])
def movies_list(request):

    data = request.GET
    user = request.user
    favourite = True if data['favourite'] == 'true' else False
    order = 'date_add' if data['order'] == 'oldest' else '-date_add'
    pagination_quantity = data['pagination']

    if favourite:
        queryset = Movie.objects.filter(user=user, favourite=favourite).order_by(order)
    else:
        queryset = Movie.objects.filter(user=user).order_by(order)

    pagination = Paginator(queryset, pagination_quantity)

    movies_list = []
    movies_id = []

    page = pagination.num_pages if int(data['page']) > pagination.num_pages else data['page']
    for movie in pagination.page(page).object_list:
        movies_id.append(movie.movie_id)
        movies_list.append({
            'movie_id': movie.movie_id,
            'favourite': movie.favourite,
            'date_add': movie.date_add
        })

    response = {
        'movies_list': movies_list,
        'movies_id': movies_id,
        'total_page': pagination.num_pages,
        'current_page': page
    }
    return Response(response)


