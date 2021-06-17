from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from sales_manager.models import Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'text', 'img', 'author', 'id', 'avg_rate']

    my_custom_field = SerializerMethodField()

    # author_name = CharField(source='author.username')
    # author = AuthorSerializer()

    # def get_my_custom_field(self, instance):
    #     return instance.text[:10] + ' hello'


class RateBookSerializer(serializers.Serializer):
    rate = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    book_id = serializers.IntegerField()

    # def validate_rate(self, instance):
    #     if instance > 5:
    #         raise serializers.ValidationError('rate must be less than 5')
    #     if instance < 0:
    #         raise serializers.ValidationError('rate must be more than 0')
    #     return instance
