# Generated by Django 3.0.4 on 2020-03-13 22:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='date_add',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
