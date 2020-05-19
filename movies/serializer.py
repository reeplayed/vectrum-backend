from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['movie_id', 'favourite', 'date_add']
