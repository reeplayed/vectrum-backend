# Generated by Django 3.0.4 on 2020-03-11 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200311_0147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='gender',
            new_name='origin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='middle_name',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
