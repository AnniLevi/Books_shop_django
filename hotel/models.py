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

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'


class RoomType(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='booked', default=1, verbose_name='Номер')
    date_from = models.DateField(verbose_name='Дата заезда')
    date_to = models.DateField(verbose_name='Дата отъезда')
    booked_person = models.ForeignKey(User, null=True, blank=True,
                                      on_delete=models.CASCADE, related_name='booked', verbose_name='Клиент')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'Бронь {self.id}'

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирование'


class Rent(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rented', verbose_name='Номер')
    start_date = models.DateField(verbose_name='Дата заезда')
    end_date = models.DateField(verbose_name='Дата отъезда')
    renter = models.ManyToManyField(User, related_name='rented', verbose_name='Клиент')

    def __str__(self):
        return f'Аренда {self.id}'

    class Meta:
        verbose_name = 'Проживание'
        verbose_name_plural = 'Проживание'


class RenterMessage(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, related_name='messages')
    # renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='Клиент')
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages', verbose_name='Номер')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return f'Сообщение {self.id}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


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