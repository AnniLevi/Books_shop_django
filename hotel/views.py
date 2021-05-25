from django.contrib.auth.decorators import login_required
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
    room.is_booked = True
    room.save()
    return redirect('hotel-page')

