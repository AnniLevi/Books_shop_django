from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, Subquery
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, GenericAPIView, \
    CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from hotel.models import Room, Booking, RoomType, TypeService, UserTypeServices, Rent, Message
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from hotel.serializers import SearchRoomSerializer, RoomSerializer, BookingCreateSerializer, OuterBookingInfoSerializer


def hotel_page(request):
    return render(request, 'hotel/index.html')


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
    ts = TypeService.objects.all()
    all_ratings = ts.exclude(avg_rate=None).aggregate(sum_all=Sum('avg_rate'), count_all=Count('avg_rate'))
    avg_all = all_ratings['sum_all'] / all_ratings['count_all']
    return render(request, 'hotel/ratings.html', {'types': ts, 'avg_all': avg_all})


@login_required
def add_rating(request, type_id, rate):
    UserTypeServices.objects.update_or_create(
        user_id=request.user.id,
        type_service_id=type_id,
        defaults={'rate': rate}
    )
    ts = TypeService.objects.get(id=type_id)
    ts.avg_rate = ts.rated_type_service.aggregate(rate=Avg('rate'))['rate']
    ts.save(update_fields=['avg_rate'])
    return redirect('hotel-rating', )


@login_required()
def profile(request):
    booking = Booking.objects.filter(booked_person_id=request.user.id). \
        prefetch_related('booked_person').order_by('date_from')
    rent_query = Rent.objects.filter(renter=request.user). \
        prefetch_related('renter').order_by('start_date')
    context = {'booking': booking, 'rent': rent_query}
    return render(request, 'hotel/profile.html', context)


@login_required()
def user_statistic(request):
    booking = Booking.objects.all().prefetch_related('booked_person').order_by('date_from')
    rent_query = Rent.objects.all().prefetch_related('renter').order_by('start_date')
    context = {'booking': booking, 'rent': rent_query}
    return render(request, 'hotel/user_statistic.html', context)


@login_required()
def user_messages(request):
    messages = Message.objects.filter(rent__renter=request.user.id).order_by('-date').select_related('rent', 'author')
    # rent = Rent.objects.filter(renter_id=request.user.id).select_related('messages')
    return render(request, 'hotel/user_messages.html', {'messages': messages})


@login_required()
def add_message(request):
    Message.objects.create(
        rent_id=request.POST['rent_number'],
        text=request.POST['text'],
        author_id=request.user.id
    )
    # messages = Message.objects.filter(rent__renter=request.user.id).select_related('rent', 'author')
    return redirect('user-messages')

@login_required()
def admin_messages(request):
    messages = Message.objects.all().order_by('-date').select_related('rent', 'author')
    return render(request, 'hotel/admin_messages.html', {'messages': messages})


class SearchRoomsAPIView(APIView):

    def post(self, request):
        search_serializer = SearchRoomSerializer(data=request.data)
        search_serializer.is_valid(raise_exception=True)
        start_date = datetime.strptime(search_serializer.data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(search_serializer.data['end_date'], '%Y-%m-%d')
        room_type = get_object_or_404(RoomType, name=search_serializer.data['room_type'])
        booked_rooms = Booking.objects.filter(
            Q(date_from__gte=start_date, date_to__lte=end_date) |
            Q(date_from__lte=start_date, date_to__gte=end_date) |
            Q(date_from__gte=start_date, date_from__lte=end_date, date_to__gte=end_date) |
            Q(date_to__gte=start_date, date_to__lte=end_date, date_from__lte=end_date)
        )
        rooms = Room.objects.filter(room_type=room_type).exclude(booked__in=booked_rooms)
        room_serializer = RoomSerializer(rooms, many=True)
        return Response(room_serializer.data, status=status.HTTP_201_CREATED)


# {"start_date":"2021-06-01", "end_date": "2021-06-10", "room_type": "3-местный"}


class RoomDetail(GenericAPIView):
    queryset = Room.objects
    serializer_class = RoomSerializer

    def get(self, request, pk):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data)


class BookingCreate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    serializer_class = BookingCreateSerializer

    def post(self, request, room_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        b_obj = Booking.objects.create(
            room_id=room_id,
            booked_person_id=request.user.id,
            **serializer.data
        )
        outer_serializer = OuterBookingInfoSerializer(b_obj)
        return Response(outer_serializer.data, status=status.HTTP_201_CREATED)

