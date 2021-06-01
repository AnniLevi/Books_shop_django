from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Room(models.Model):
    number = models.IntegerField(primary_key=True, verbose_name='Номер')
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, default=None)
    room_area = models.FloatField(verbose_name='Площадь')
    is_lux = models.BooleanField(verbose_name='Люкс')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=False, verbose_name='Цена')
    booked_person = models.ManyToManyField(User, through='Booking', related_name='booked_room')

    def __str__(self):
        return f'Номер {self.number}'


class RoomType(models.Model):
    name = models.CharField(max_length=20, primary_key=True)


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='booked', default=1)
    date_from = models.DateField()
    date_to = models.DateField()
    booked_person = models.ForeignKey(User, null=True, blank=True,
                                      on_delete=models.CASCADE, related_name='booked')
    description = models.TextField(null=True, blank=True)


class Rent(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rented')
    start_date = models.DateField()
    end_date = models.DateField()
    renter = models.ManyToManyField(User, related_name='rented')


class RenterMessage(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()


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