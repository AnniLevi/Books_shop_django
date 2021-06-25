from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import CharField

from hotel.models import Booking, Room, RoomType, Message


class SearchRoomSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    room_type = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff']


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('name',)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    room_type = RoomTypeSerializer()
    booked_person = UserSerializer(many=True)


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['date_from', 'date_to', 'description']


class OuterBookingInfoSerializer(serializers.ModelSerializer):
    # room = RoomSerializer()
    booked_person = UserSerializer()

    class Meta:
        model = Booking
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'