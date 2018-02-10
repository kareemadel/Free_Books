from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Author
from django.views import generic


# Create your views here.
class home_view(TemplateView):
    def get(self, request):
        return render(request, 'FreeBooks/HomePage.html')


class authorsListView(generic.ListView):
	model=Author

class authorsDetailView(generic.DetailView):
    model = Author
