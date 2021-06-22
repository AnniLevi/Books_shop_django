from django.urls import path
from hotel import views

urlpatterns = [
    path('filter/', views.filter_room, name='filter-room'),
    path('search/', views.search_room, name='search-room'),
    path('room_detail/<int:room_id>/', views.room_detail, name='room-detail'),
    path('room_booking/<int:room_id>/', views.booking_the_room, name='room-booking'),
    path('ratings/', views.rating_page, name='hotel-rating'),
    path('add_rating/<int:type_id>/<int:rate>/', views.add_rating, name='add-rating'),
    path('profile/', views.profile, name='profile'),
    path('profile/user_messages/', views.user_messages, name='user-messages'),
    path('profile/user_messages/add_message/', views.add_message, name='add-message'),
    path('user_statistic/', views.user_statistic, name='user-statistic'),
    path('user_statistic/admin_messages', views.admin_messages, name='admin-messages'),
    path('search_room_api/', views.SearchRoomsAPIView.as_view()),
    path('search_room_api/<int:pk>', views.RoomDetail.as_view()),
    path('booking_create/<int:room_id>', views.BookingCreate.as_view()),
    path('', views.hotel_page, name='hotel-page'),
]
