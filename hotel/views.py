from django.shortcuts import render
from hotel.models import Room


def main_page(request):
    query_set = Room.objects.all()
    context = {'all_rooms': query_set}
    return render(request, 'hotel/index.html', context=context)


def room_detail(request, room_id):
    room = Room.objects.get(number=room_id)
    context = {'room': room}
    return render(request, 'hotel/room_detail.html', context)
