# Generated by Django 3.2.3 on 2021-06-01 12:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel', '0005_occupation_rentermessage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Occupation',
            new_name='Rent',
        ),
    ]