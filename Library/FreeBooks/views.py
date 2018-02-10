from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from .models import Book

# Create your views here.
class home_view(TemplateView):
    def get(self, request):
        return render(request, 'FreeBooks/base.html')


class book_view(DetailView):
    model = Book

class book_list_view(ListView):
    model = Book