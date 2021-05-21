from django.shortcuts import render
from hotel.models import Room


def main_page(request):
    query_set = Room.objects.all()
    context = {'all_rooms': query_set}
    return render(request, 'hotel/index.html', context=context)
