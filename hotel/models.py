from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Room(models.Model):
    number = models.IntegerField(primary_key=True, verbose_name='Номер')
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, default=None, verbose_name='Тип')
    room_area = models.FloatField(verbose_name='Площадь')
    is_lux = models.BooleanField(verbose_name='Люкс')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=False, verbose_name='Цена')
    booked_person = models.ManyToManyField(User, through='Booking', related_name='booked_room')
    image = models.ImageField(upload_to='hotel/photos/%Y/%m/%d/', blank=True, verbose_name='Изображение')

    def __str__(self):
        return f'Номер {self.number}'

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        ordering = ('number', )


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


class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, related_name='messages', default=1)
    # renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='Клиент')
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages', verbose_name='Номер')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return f'Сообщение {self.id}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class TypeService(models.Model):
    class Meta:
        verbose_name = 'Тип сервиса'
        verbose_name_plural = 'Типы сервиса'

    title = models.CharField(max_length=50, unique=True, verbose_name='Название')
    avg_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Средний балл'
    )
    user = models.ManyToManyField(
        User,
        related_name='rated_services',
        blank=True
    )

    def __str__(self):
        return self.title


class UserTypeServices(models.Model):
    class Meta:
        unique_together = ('user', 'type_service')

    user = models.ForeignKey(
        User,
        related_name='rated_type_service',
        on_delete=models.SET_DEFAULT,
        default=4
    )
    type_service = models.ForeignKey(
        TypeService,
        on_delete=models.CASCADE,
        related_name='rated_type_service'
    )
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

