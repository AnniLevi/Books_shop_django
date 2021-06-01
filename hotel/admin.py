from django.contrib import admin
from hotel.models import Room, RoomType, Booking, Rating, Rent, RenterMessage


class RenterMessageInline(admin.TabularInline):
    model = RenterMessage
    readonly_fields = ('date', 'text',)
    ordering = ('date',)
    # list_display = ('date', 'text', 'rent.room')


class RentAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_date', 'end_date')
    inlines = (RenterMessageInline,)


admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Rating)
admin.site.register(Rent, RentAdmin)
admin.site.register(RenterMessage)
