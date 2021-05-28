from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from hotel.models import Room, Booking, Rating


def hotel_page(request):
    query_set = Room.objects.all()
    context = {'all_rooms': query_set}
    return render(request, 'hotel/index.html', context=context)


def room_detail(request, room_id):
    room = Room.objects.get(number=room_id)
    context = {'room': room}
    return render(request, 'hotel/room_detail.html', context)


@login_required
def booking_the_room(request, room_id):
    room = Room.objects.get(number=room_id)
    Booking.objects.create(
        room_number=room,
        date_from=request.POST['date_from'],
        date_to=request.POST['date_to'],
        booked_person=request.user,
        description=request.POST['description']
    )
    return redirect('hotel-page')


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
