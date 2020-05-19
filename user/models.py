from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core import validators
from django.db.models.signals import pre_save
from .utils import set_random_image


class CustomUser(AbstractUser):

    username = models.CharField(
        ('username'),
        max_length=100,
        unique=True,
        help_text=('Required. 30 characters or fewer. Letters, digits and '
                   '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                ('Enter a valid username. '
                 'This value may contain only letters, numbers '
                 'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': ("A user with that username already exists."),
        })

    email = models.EmailField(

        ('email address'),
        unique=True,
        error_messages={
            'unique': ("A user with that email already exists."),
        })

    first_name = models.CharField(('first name'), max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    is_active = models.BooleanField(default=True)
    google_id = models.CharField(max_length=200, unique=True, null=True, blank=True)
    profile_image = models.CharField(max_length=300, null=True, blank=True)
    google_password = models.CharField(max_length=200, unique=True, null=True, blank=True)
    origin = models.CharField(max_length=10, null=True, blank=True)


def user_pre_save(sender, instance, *args, **kwargs):
    if instance.origin == 'google':
        instance.set_password(instance.google_password)
    if not instance.profile_image:
        instance.profile_image = set_random_image()


pre_save.connect(user_pre_save, sender=CustomUser)


