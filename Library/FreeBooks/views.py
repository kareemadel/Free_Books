from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from .models import Book, Category, Author, Profile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
class home_view(TemplateView):
    def get(self, request):
        return render(request, 'FreeBooks/HomePage.html')


class book_view(DetailView):
    model = Book

class book_list_view(ListView):
    model = Book

class category_list_view(ListView):
    model = Category


class category_view(DetailView):
    model = Category

class authorsListView(ListView):
    model=Author

class authorsDetailView(DetailView):
    model = Author

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'bio', 'pic')

@transaction.atomic
def create_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user_id = user.id
            profile.favourite_category = Category.objects.get(pk=2)
            profile.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('FreeBooks:home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'FreeBooks/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })