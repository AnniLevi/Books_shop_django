from django.urls import path
from hotel import views

urlpatterns = [
    path('filter/', views.filter_room, name='filter-room'),
    path('search/', views.search_room, name='search-room'),
    path('room_detail/<int:room_id>/', views.room_detail, name='room-detail'),
    path('room_booking/<int:room_id>/', views.booking_the_room, name='room-booking'),
    path('ratings/', views.rating_page, name='hotel-rating'),
    path('add_rating/<int:type_id>/<int:rate>/', views.add_rating, name='add-rating'),
    path('', views.hotel_page, name='hotel-page'),
]



