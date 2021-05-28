from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Room(models.Model):
    number = models.IntegerField(primary_key=True, verbose_name='Номер')
    number_of_people = models.IntegerField(null=False, default=1, verbose_name='Вмещает людей')
    room_area = models.FloatField(null=False, verbose_name='Площадь')
    is_lux = models.BooleanField(default=False, verbose_name='Люкс')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=False, verbose_name='Цена')

    def __str__(self):
        return f'Номер {self.number}'


class Rating(models.Model):
    service_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                          verbose_name='Качество обслуживания')
    cleanness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                    verbose_name='Чистота')
    friendliness_of_staff = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                                verbose_name='Приветливость персонала')
    equipment_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                            verbose_name='Качество оборудования')
    food_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                       verbose_name='Качество еды')
    location = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                   verbose_name='Расположение')
    territory_condition = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                              verbose_name='Состояние прилегающей территории')
    rating_person = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, related_name='ratings')


class Booking(models.Model):
    room_number = models.ForeignKey(Room, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='booking_room')
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    booked_person = models.ForeignKey(User, null=True, blank=True,
                                      on_delete=models.SET_NULL, related_name='booking_user')
    description = models.TextField(null=True, blank=True)
