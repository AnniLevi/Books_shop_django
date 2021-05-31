from django.contrib import admin
from hotel.models import Room, RoomType, Booking, Rating

admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Booking)
admin.site.register(Rating)

