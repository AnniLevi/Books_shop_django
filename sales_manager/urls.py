from django.urls import path
from sales_manager import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('book_detail/<int:book_id>/', views.book_detail, name='book-detail'),
    path('book_rate/<int:book_id>/<int:rate>/<str:redirect_url>/', views.book_like, name='book-rate'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('add-ajax-like/', views.add_like_ajax),
    path('add-ajax-like/', views.AddLikeCommentAPIView.as_view()),
    path('add_comment/<int:book_id>/', views.add_comment, name='add-comment'),
    path('comment_like/<int:comment_id>/', views.comment_like, name='comment-like'),
    path('show_all_books/', cache_page(60 * 10)(views.BookListAPIView.as_view())),
    path('show_all_books/<int:pk>/', views.BookDetail.as_view()),
    path('update_book/<int:pk>/', views.BookUpdateAPIView.as_view()),
    path('add_rate_book_api/', views.AddRateBook.as_view(), name='add-rate-book'),
    path('create_book/', views.BookCreate.as_view(), name='create-book'),
    path('', views.main_page, name='main-page')
]
