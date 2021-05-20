from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    number = models.IntegerField(primary_key=True, verbose_name='Номер')
    number_of_people = models.IntegerField(null=False, default=1, verbose_name='Вмещает людей')
    room_area = models.FloatField(null=False, verbose_name='Площадь')
    is_lux = models.BooleanField(default=False, verbose_name='Люкс')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=False, verbose_name='Цена')
    is_booked = models.BooleanField(default=False, verbose_name='Забронировано')
    booked_from = models.DateField(null=True, blank=True)
    booked_to = models.DateField(null=True, blank=True)
    booked_person = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.number
