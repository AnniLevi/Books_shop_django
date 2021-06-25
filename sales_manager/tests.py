from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from sales_manager.models import Book
import json


class CRUDBookTest(TestCase):

    def setUp(self):  # запускается перед стартом каждого теста
        self.user = User.objects.create_user('test name')

    def test_create_book(self):
        self.client.force_login(self.user)  # self.client - клиентская часть
        url = reverse('create-book')  # возвращает урл по имени эндпоинта
        data = {
            'title': 'test title',
            'text': 'test text',
            'author': self.user.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['text'], data['text'])
        self.assertEqual(response.data['author'], data['author'])
        book = Book.objects.get(**data)  # .get(title='test title', text='test text', ...)
        self.assertEqual(response.data['id'], book.id)

    def test_update(self):
        book = Book.objects.create(title='test title', text='test text', author=self.user)
        self.client.force_login(self.user)


class SetRateBookTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('test name')
        self.user2 = User.objects.create_user('test name2')
        self.book = Book.objects.create(
            title='test title',
            text='test text',
            author=self.user1
        )

    def test_rate(self):
        self.client.force_login(self.user1)
        url = reverse('add-rate-book')
        data = {
            'rate': 3,
            'book_id': self.book.id
        }
        # good case
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)  # msg если assert завалится
        self.assertEqual(response.data['avg_rate'], 3)
        # check other user good case
        self.client.force_login(self.user2)
        data['rate'] = 5
        response = self.client.put(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(response.data['avg_rate'], 4)
        # check 400 msg
        data.pop('rate')
        response = self.client.put(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        self.assertEqual(
            response.data['rate'][0],
            ErrorDetail(string='Обязательное поле.', code='required')
        )
        # check 400 again
        data['rate'] = 50
        response = self.client.put(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        # check 401 msg
        self.client.logout()
        data['rate'] = 5
        response = self.client.put(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
