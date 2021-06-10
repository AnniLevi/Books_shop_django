from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from sales_manager.models import Book


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BookSerializer(ModelSerializer):
    my_custom_field = SerializerMethodField()
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['title', 'text', 'img', 'my_custom_field', 'author']

    def get_my_custom_field(self, instance):
        return instance.text[10:] + 'hello'

