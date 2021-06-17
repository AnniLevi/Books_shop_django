from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sales_manager.models import Book, Comment, UserRateBook
from sales_manager.paginators import MyPagination
from sales_manager.serializers import BookSerializer, CreateBookSerializer
from sales_manager.utils import get_books_with_comment
from sales_manager.serializers import RateBookSerializer



def main_page(request):
    query_set = get_books_with_comment()
    context = {'books': query_set}
    return render(request, 'sales_manager/index.html', context=context)


def book_detail(request, book_id):
    query_set = get_books_with_comment()
    book = query_set.get(id=book_id)
    context = {'book': book}
    return render(request, 'sales_manager/book_detail.html', context=context)


@login_required()
def book_like(request, book_id, rate, redirect_url):
    UserRateBook.objects.update_or_create(
        user_id=request.user.id,
        book_id=book_id,
        defaults={"rate": rate}
    )
    book = Book.objects.get(id=book_id)
    book.avg_rate = book.rated_user.aggregate(rate=Avg('rate'))['rate']
    book.save(update_fields=['avg_rate'])
    if redirect_url == 'main-page':
        return redirect('main-page')
    elif redirect_url == 'book-detail':
        return redirect('book-detail', book_id=book_id)


class LoginView(View):
    def get(self, request):
        return render(request, 'sales_manager/login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST['login'],
            password=request.POST['pwd']
        )
        if user is not None:
            login(request, user)
            return redirect('main-page')
        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('main-page')


@login_required()
@require_http_methods(['POST'])
def add_comment(request, book_id):
    text = request.POST.get('text')
    Comment.objects.create(
        text=text,
        user_id=request.user.id,
        book_id=book_id
    )
    return redirect('book-detail', book_id=book_id)


@login_required()
def comment_like(request, comment_id):
    com = Comment.objects.get(id=comment_id)
    if request.user in com.like.all():
        com.like.remove(request.user)
    else:
        com.like.add(request.user)
    return redirect('book-detail', bood_id=com.book_id)


def add_like_ajax(request):
    comment_id = request.POST['comment_id']
    query_com = Comment.objects.filter(id=comment_id)
    if query_com.exists():
        com = query_com.first()
        if request.user in com.like.all():
            com.like.remove(request.user)
        else:
            com.like.add(request.user)
        return HttpResponse(com.like.count())
    return HttpResponseNotFound('error')


# only GET-method
# class BookListAPIView(ListAPIView):
#     queryset = Book.objects.all().select_related('author')
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]


# another variant - GET and POST, implemented manually
# class BookListAPIView(APIView):
#
#     def get(self, request):
#         query_set = Book.objects.all()
#         serializer = BookSerializer(query_set, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = BookSerializer(request.data)
#         if serializer.is_valid():
#             book = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# third variant - GET and POST
class BookListAPIView(ListCreateAPIView):
    pagination_class = MyPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    queryset = Book.objects
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'text', 'author__username')
    ordering_fields = ('id', 'title', 'author__id')
    ordering = ('-id', )

    # def list(self, request, pk=None, **kwargs):
    #     if pk is not None:
    #         serializer = self.serializer_class(self.get_object())
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


class BookDetail(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # lookup_field = 'title'

    def get(self, request, pk):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data)


class BookUpdateAPIView(RetrieveUpdateDestroyAPIView):
    '''test description'''
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateBookSerializer


class AddRateBook(APIView):
    serializer_class = RateBookSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # аналогично:
        serializer.is_valid(raise_exception=True)
        # query_set_book = Book.objects.filter(id=serializer.data['book_id'])
        # if not query_set_book.exists():
        #     return Response({}, status=status.HTTP_404_NOT_FOUND)
        # аналогично:
        book = get_object_or_404(Book, id=serializer.data['book_id'])
        UserRateBook.objects.update_or_create(
            user_id=request.user.id,
            book_id=book.id,
            defaults={"rate": serializer.data['rate']}
        )
        book.avg_rate = book.rated_user.aggregate(rate=Avg('rate'))['rate']
        book.save(update_fields=['avg_rate'])
        return Response({'avg_rate': book.avg_rate}, status=status.HTTP_201_CREATED)
