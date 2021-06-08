from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views import View
from django.db.models import Avg
from sales_manager.models import Book, Comment, UserRateBook
from sales_manager.utils import get_books_with_comment
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from sales_manager.serializers import BookSerializer


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


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]