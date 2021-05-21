from django.urls import path
from hotel import views

urlpatterns = [
    path('room_detail/<int:room_id>/', views.room_detail, name='room_detail'),
    path('', views.main_page),
]
