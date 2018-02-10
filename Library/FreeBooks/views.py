from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from .models import Book, Category

# Create your views here.
class home_view(TemplateView):
    def get(self, request):
        return render(request, 'FreeBooks/base.html')


class book_view(DetailView):
    model = Book

class book_list_view(ListView):
    model = Book

class category_list_view(ListView):
    model = Category


class category_view(DetailView):
    model = Category
