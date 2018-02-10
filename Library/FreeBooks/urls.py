
from django.urls import path
from .views import home_view, book_view

app_name = 'FreeBooks'

urlpatterns = [
    path('', home_view.as_view(), name='home'),
    path('books/<pk>', book_view.as_view(), name='book_detail')
]