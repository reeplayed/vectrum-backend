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
@permission_classes([AllowAny])
def ship(request):
    
    ships = [5, 4, 3, 3,5, 2, 2, 2]

    output_choices = []

    output_borders = {}

    ships_dementions = {}

    scope = [i for i in range(0, 10)]

    all = []

    for i in scope:
        for j in scope:
            all.append([i,j])

    directions = [(0,1), (0, -1), (1, 0), (-1, 0)]

    def valid(array, all, choices):
            for element in array:
                if (element not in all) or (element in choices):
                    return False
            return True

    border = []
    choices = []

    index = 1

    for length in ships:

        isFind = False

        repeatings = []

        cyclic_border = []

        cyclic_choice = []

        while not isFind:
            rand = random.choice(all) # all-choices-border
           
            random.shuffle(directions)

            for dir in directions:

                drct = [ [rand[0]+i*dir[0], rand[1]+i*dir[1]] for i in range(1, length+1)]
                
                if valid(drct, all, choices+border):
                    
                    ships_dementions[f'ship{index}'] = length

                    choices += drct
                    output_choices += [ { 'idx':(i[0]*len(scope)+i[1]), 'name': f'ship{index}', 'hit': False} for i in drct]

                    cyclic_border.append([  drct[0][0]-dir[0] , drct[0][1]-dir[1]       ])
                    cyclic_border.append([  drct[len(drct)-1][0]+dir[0] , drct[len(drct)-1][1]+dir[1]       ])
                    
                    for item in range(-1,len(drct)+1):
                        cyclic_border.append([      rand[0]+dir[1]+dir[0]*(item+1), rand[1]+dir[0]+dir[1]*(item+1)    ])
                        cyclic_border.append([      rand[0]-dir[1]+dir[0]*(item+1), rand[1]-dir[0]+dir[1]*(item+1)    ])
                    
                    output_borders[f'ship{index}'] = []
                    
                    for i in cyclic_border:
                        if (i[0] in scope) and (i[1] in scope):
                            output_borders[f'ship{index}'].append((i[0]*len(scope)) + i[1])


                    index += 1

                    border += cyclic_border
                    isFind = True
                    break
            repeatings.append(rand)

    randoms = [ (i[0]*len(scope))+i[1] for i in choices]
    
    final_output = []

    for i in range(0,100):
        if i not in randoms:
            final_output.append({'idx': i, 'name': '', 'hit': False})
       
    final_output += output_choices

    final_output = sorted(final_output, key = lambda i: (i['idx'])) 

    # all = [ i[0]*10+i[1] for i in all]
    # randoms = [ (i[0]*len(scope))+i[1] for i in choices]
    # border = [ ((i[0]*len(scope)) if i[0] in scope else 1000) + (i[1] if i[1] in scope else 1000) for i in border]

    res = {
        'array' : final_output,
        'ships': ships_dementions,
        'border': output_borders
    }

    return Response(res)
    













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




# @api_view(['POST'])
# def remove_all_movies(request):
#     data = request.data
#     user = request.user
#
#     if data['all']:
#         Movie.objects.filter(user=user).delete()
#         return Response({'message': 'Successfully has removed all movies.'})
#     else:
#         try:
#             Movie.objects.get(user=user, movie_id=data['movie_id']).delete()
#             return Response({'message': 'Successfully has removed movie.'})
#         except Movie.DoesNotExist:
#             return Response({'status': 'false', 'message': "Movie does not exist.."}, status=401)
#
#     return Response({'status': 'false', 'message': "Something has wrong."}, status=401)

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


