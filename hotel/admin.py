from django.contrib import admin
from hotel.models import Room, RoomType, Booking, Rent, TypeService, Message


class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'room_type', 'is_lux')


class RentAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_date', 'end_date')


class TypeServiceAdmin(admin.ModelAdmin):
    exclude = ('user', )
    readonly_fields = ('avg_rate', )
    list_display = ('title', 'avg_rate', )


admin.site.register(Room,RoomAdmin)
admin.site.register(RoomType)
admin.site.register(Booking)
admin.site.register(Rent, RentAdmin)
admin.site.register(TypeService, TypeServiceAdmin)
admin.site.register(Message)
