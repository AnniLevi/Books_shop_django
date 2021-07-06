from django.contrib import admin
from hotel.models import Room, RoomType, Booking, Rent, TypeService, Message


class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'room_type', 'is_lux')


class RentAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_date', 'end_date')


@admin.register(TypeService)
class TypeServiceAdmin(admin.ModelAdmin):
    exclude = ('user', )
    readonly_fields = ('avg_rate', )
    list_display = ('title', 'avg_rate', )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'rent', 'author', 'text')
    list_display_links = ('id', 'text')


admin.site.register(Room,RoomAdmin)
admin.site.register(RoomType)
admin.site.register(Booking)
admin.site.register(Rent, RentAdmin)
# admin.site.register(TypeService, TypeServiceAdmin)
admin.site.register(Message, MessageAdmin)
