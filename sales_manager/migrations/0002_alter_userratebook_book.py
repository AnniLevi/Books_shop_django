# Generated by Django 3.2.3 on 2021-05-30 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userratebook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_user', to='sales_manager.book'),
        ),
    ]
