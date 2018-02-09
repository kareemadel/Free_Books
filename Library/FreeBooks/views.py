from django.shortcuts import render
from django.views.generic import TemplateView

app_name = 'FreeBooks'

# Create your views here.
class home_view(TemplateView):
    def get(self, request):
        return render(request, 'FreeBooks/base.html')