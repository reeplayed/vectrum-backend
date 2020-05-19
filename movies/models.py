from django.db import models
from django.contrib.auth import settings
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Movie(models.Model):
    movie_id = models.CharField(max_length=120)
    favourite = models.BooleanField(default=False)
    date_add = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie_id
