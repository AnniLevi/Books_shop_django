from django.contrib import admin
from hotel.models import Room, RoomType, Booking, Rent, RenterMessage, TypeService


class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'room_type', 'is_lux')


class RenterMessageInline(admin.TabularInline):
    model = RenterMessage
    readonly_fields = ('date', 'text',)
    ordering = ('date',)


class RentAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_date', 'end_date')
    inlines = (RenterMessageInline,)


class TypeServiceAdmin(admin.ModelAdmin):
    exclude = ('user', )
    readonly_fields = ('avg_rate', )
    list_display = ('title', 'avg_rate', )


admin.site.register(Room,RoomAdmin)
admin.site.register(RoomType)
admin.site.register(Booking)
admin.site.register(Rent, RentAdmin)
admin.site.register(RenterMessage)
admin.site.register(TypeService, TypeServiceAdmin)
