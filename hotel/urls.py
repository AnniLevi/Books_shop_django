from django.urls import path
from hotel import views

urlpatterns = [
    path('room_detail/<int:room_id>/', views.room_detail, name='room-detail'),
    path('room_booking/<int:room_id>/', views.booking_the_room, name='room-booking'),
    path('', views.hotel_page, name='hotel-page'),
]
