# Generated by Django 3.2.3 on 2021-05-31 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_auto_20210531_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='type',
            new_name='room_type',
        ),
    ]
