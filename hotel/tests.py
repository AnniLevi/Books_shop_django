from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from hotel.models import Room, RoomType, Booking, Rent
import json

class SearchRoomsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_name')
        self.room_type = RoomType.objects.create(name='2-местный')
        self.room = Room.objects.create(
            number=1,
            room_type_id=self.room_type.name,
            room_area=25.5,
            is_lux=False,
            price=100
        )
        self.room2 = Room.objects.create(
            number=2,
            room_type_id=self.room_type.name,
            room_area=25.5,
            is_lux=False,
            price=100
        )

    def test_search_rooms(self):
        Booking.objects.create(
            room=self.room2,
            date_from="2021-05-20",
            date_to="2021-06-06",
            booked_person=self.user
        )
        url = reverse('search-room-api')
        data = {
            "start_date": "2021-06-01",
            "end_date": "2021-06-10",
            "room_type": "2-местный"
        }
        response = self.client.post(url, data)
        # check 200 msg
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        # check correct response fields
        self.assertEqual(response.data[0]['number'], self.room.number)
        self.assertEqual(response.data[0]['room_type']['name'], self.room_type.name)
        # check room2 is not in response
        self.assertEqual(len(response.data), 1)
        # check room in response
        Booking.objects.create(
            room=self.room,
            date_from="2021-06-11",
            date_to="2021-06-15",
            booked_person=self.user
        )
        response = self.client.post(url, data)
        self.assertEqual(response.data[0]['number'], self.room.number)
        self.assertEqual(response.data[0]['room_type']['name'], self.room_type.name)
        # check room not in response
        Booking.objects.create(
            room=self.room,
            date_from="2021-06-02",
            date_to="2021-06-05",
            booked_person=self.user
        )
        response = self.client.post(url, data)
        self.assertEqual(len(response.data), 0)

    def test_room_detail(self):
        url = reverse('room-datail-api', args=[self.room.number])
        response = self.client.get(url)
        self.assertEqual(response.data['number'], self.room.number)
        self.assertEqual(response.data['room_type']['name'], self.room_type.name)
        self.assertEqual(response.data['room_area'], self.room.room_area)
        self.assertEqual(response.data['is_lux'], self.room.is_lux)
        self.assertEqual(response.data['price'], self.room.price)


class BookingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_name')
        self.room_type = RoomType.objects.create(name='2-местный')
        self.room = Room.objects.create(
            number=1,
            room_type_id=self.room_type.name,
            room_area=25.5,
            is_lux=False,
            price=100
        )

    def test_booking_create(self):
        url = reverse('booking-create', args=[self.room.number])  # or kwargs={'room_id': room.number}
        self.client.force_login(self.user)
        data = {
            'room_id': self.room.number,
            'booked_person_id': self.user.id,
            'date_from': '2021-06-01',
            'date_to': '2021-06-10'
        }
        response = self.client.post(url, data)
        # check 201 msg
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        # check correct object's fields
        self.assertEqual(response.data['room'], data['room_id'])
        self.assertEqual(response.data['date_from'], data['date_from'])
        self.assertEqual(response.data['date_to'], data['date_to'])
        self.assertEqual(response.data['booked_person']['id'], data['booked_person_id'])
        booking_obj = Booking.objects.get(**data)
        self.assertEqual(response.data['id'], booking_obj.id)


class MessageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_name')
        self.room_type = RoomType.objects.create(name='2-местный')
        self.room = Room.objects.create(
            number=1,
            room_type_id=self.room_type.name,
            room_area=25.5,
            is_lux=False,
            price=100
        )
        self.rent = Rent.objects.create(
            room=self.room,
            start_date='2021-06-01',
            end_date='2021-06-10',
        )
        self.rent.renter.add(self.user)

    def test_message_create(self):
        self.client.force_login(self.user)
        data = {
            "text": "test text",
            "rent_id": self.rent.id,
            "author_id": self.user
        }
        url = reverse('message-create')
        response = self.client.post(url, data)
        # check 201 msg
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        # good case
        self.assertEqual(response.data['author'], data['author_id'].id)
        self.assertEqual(response.data['rent'], data['rent_id'])
        self.assertEqual(response.data['text'], data['text'])
        # check 400 msg
        data.pop('text')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        self.assertEqual(
            response.data['text'][0],
            ErrorDetail(string='Обязательное поле.', code='required')
        )
        # check 401 or 403 msg
        self.client.logout()
        data['text'] = "test text"
        response = self.client.post(url, data=data)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
            msg=response.data
        )

    def test_message_update(self):
        self.client.force_login(self.user)
        data = {
            "text": "test text",
            "rent_id": self.rent.id,
            "author_id": self.user.id
        }
        create_response = self.client.post(reverse('message-create'), data)
        url = reverse('message-update', args=[create_response.data['id']])
        # check get method
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        # check put method
        data['text'] = 'text2'
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data['text'], data['text'])
        self.assertEqual(response.data['author'], data['author_id'])
        self.assertEqual(response.data['rent'], data['rent_id'])
        # check patch method
        data['text'] = 'text3'
        response = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data['text'], data['text'])
        self.assertEqual(response.data['author'], data['author_id'])
        self.assertEqual(response.data['rent'], data['rent_id'])
        # check 401 or 403 msg
        self.client.logout()
        data['text'] = "test text"
        response = self.client.post(url, data=data)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
            msg=response.data
        )
        # check 400 msg
        self.client.force_login(self.user)
        data.pop('text')
        response = self.client.put(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        self.assertEqual(
            response.data['text'][0],
            ErrorDetail(string='Обязательное поле.', code='required')
        )
        # check delete method
        response = self.client.delete(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)
        # check 404 msg
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.data)



# pip install coverage
# coverage run --source='.' manage.py test
# coverage run --source='.' manage.py test the-app-you-want-to-test
# coverage report  - в командной строке
# coverage html   - в html файл
