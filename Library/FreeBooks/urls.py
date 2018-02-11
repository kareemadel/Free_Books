from django.urls import path
from .views import home_view, book_view, book_list_view, category_list_view, category_view, authorsListView, authorsDetailView, create_profile

app_name = 'FreeBooks'

urlpatterns = [
    path('', home_view.as_view(), name='home'),
    path('books/<pk>', book_view.as_view(), name='book_detail'),
    path('books/', book_list_view.as_view(), name='book_list'),
    path('categories/', category_list_view.as_view(), name='category_list'),
    path('categories/<pk>', category_view.as_view(), name='category_detail'),
    path('authors/', authorsListView.as_view(), name='AuthorList'),
    path('authors/<int:pk>', authorsDetailView.as_view(), name='AuthorDetail'),
    path('register/', create_profile, name='register'),
]