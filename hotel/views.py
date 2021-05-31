from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from hotel.models import Room, Booking, Rating, RoomType
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.db.models import Q


def filter_room(request):
    room_type = RoomType.objects.all()
    return render(request, 'hotel/filter_form.html', {'room_types': room_type})


def search_room(request):
    start_date = datetime.strptime(request.GET['date_from'], '%Y-%m-%d')
    end_date = datetime.strptime(request.GET['date_to'], '%Y-%m-%d')
    room_type = request.GET['room_type']
    booked_rooms = Booking.objects.filter(
        Q(date_from__gte=start_date, date_to__lte=end_date) |
        Q(date_from__lte=start_date, date_to__gte=end_date) |
        Q(date_from__gte=start_date, date_from__lte=end_date, date_to__gte=end_date) |
        Q(date_to__gte=start_date, date_to__lte=end_date, date_from__lte=end_date)
    )
    rooms = Room.objects.filter(room_type=room_type).exclude(booked__in=booked_rooms)
    # rooms = Room.objects.filter(Q(room_type=room_type) & ~Q(booked__in=booked_rooms))
    return render(request, 'hotel/search.html', {'rooms': rooms})


def room_detail(request, room_id):
    room = Room.objects.get(number=room_id)
    context = {'room': room}
    return render(request, 'hotel/room_detail.html', context)


@login_required
@require_http_methods(['POST'])
def booking_the_room(request, room_id):
    Booking.objects.create(
        room_id=room_id,
        date_from=request.POST['date_from'],
        date_to=request.POST['date_to'],
        booked_person=request.user,
        description=request.POST['description']
    )
    return redirect('filter-room')


def rating_page(request):
    context = Rating.objects.all().aggregate(
        avg_service_quality=Avg('service_quality'),
        avg_cleanness=Avg('cleanness'),
        avg_friendliness_of_staff=Avg('friendliness_of_staff'),
        avg_equipment_quality=Avg('equipment_quality'),
        avg_food_quality=Avg('food_quality'),
        avg_location=Avg('location'),
        avg_territory_condition=Avg('territory_condition'),
    )
    s = 0
    for value in context.values():
        s += float(value)
    avg_all = s / 7
    context['avg_all'] = avg_all
    return render(request, 'hotel/ratings.html', context=context)


@login_required
def add_rating(request):
    Rating.objects.update_or_create(
        rating_person_id=request.user.id,
        defaults={'service_quality': request.POST['service_quality'],
                  'cleanness': request.POST['cleanness'],
                  'friendliness_of_staff': request.POST['friendliness_of_staff'],
                  'equipment_quality': request.POST['equipment_quality'],
                  'food_quality': request.POST['food_quality'],
                  'location': request.POST['location'],
                  'territory_condition': request.POST['territory_condition'],
                  }
    )
    return redirect('hotel-rating')
