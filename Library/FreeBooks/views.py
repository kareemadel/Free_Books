from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, ListView
from .models import Book, Category, Author, Profile, Read, Rate, WishList
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse
import json


# Create your views here.
class home_view(TemplateView):
    def get(self, request):
        return render(request, 'FreeBooks/HomePage.html')


class book_view(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id

        user = Profile.objects.filter(user_id=current_user)
        user = len(user) and user[0]

        read = Read.objects.filter(user_id=current_user)
        read = len(read) and read[0]

        rate = Rate.objects.filter(user_id=current_user)
        rate = len(rate) and rate[0].score
        rate_list = []
        rate_title = ('Poor', 'Fair', 'Good', 'Excellent', 'WOW!!!')
        for i in range(rate):
            rate_list.append(('star selected', rate_title[i], i + 1))
        for j in range(5 - rate):
            rate_list.append(('star', rate_title[j + rate], j + rate + 1))

        wish = WishList.objects.filter(user_id=current_user)
        wish = len(wish) and wish[0]

        context.update({
            'read': read,
            'wish': wish,
            'rate': rate_list,
        })
        return context

    def post(self, request, **kwargs):
        body = json.loads(self.request.body.decode("utf-8"))
        print(body)
        for field in body:
            if field == 'rate':
                Rate.objects.update_or_create(user_id=self.request.user.id, book_id=self.kwargs['pk'], defaults={'score': body[field]})

            elif field =='read' and body[field]:
                Read.objects.get_or_create(user_id=self.request.user.id, book_id=self.kwargs['pk'])
                wishRecord = WishList.objects.filter(user_id=self.request.user.id, book_id=self.kwargs['pk'])
                if wishRecord.exists():
                    wishRecord[0].delete()

            elif field == 'unread' and body[field]:
                readRecord = Read.objects.filter(user_id=self.request.user.id, book_id=self.kwargs['pk'])
                if readRecord.exists():
                    readRecord[0].delete()

            elif field == 'wish' and body[field]:
                WishList.objects.get_or_create(user_id=self.request.user.id, book_id=self.kwargs['pk'])
                readRecord = Read.objects.filter(user_id=self.request.user.id, book_id=self.kwargs['pk'])
                if readRecord.exists():
                    readRecord[0].delete()

            elif field == 'unwish' and body[field]:
                wishRecord = WishList.objects.filter(user_id=self.request.user.id, book_id=self.kwargs['pk'])
                if wishRecord.exists():
                    wishRecord[0].delete()

        return HttpResponse("hello")



class book_list_view(ListView):
    model = Book

class category_list_view(ListView):
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
            profile.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('FreeBooks:home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'FreeBooks/registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

class Search(ListView):

    class Meta:
        verbose_name = "Search"
        verbose_name_plural = "Searches"

    template_name = 'FreeBooks/search.html'
    context_object_name = 'character_series_list'
    model = Book

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q', '')
        context = super().get_context_data(**kwargs)
        context.update({
            'book_list': Book.objects.filter(title__icontains=q),
            'author_list': Author.objects.filter(name__icontains=q),
        })
        return context

    def __str__(self):
        pass

class book_author_list(ListView):
    model = Book
    context_object_name = 'book_author_list'
    template_name = 'FreeBooks/book_author_list.html'
    def get_queryset(self, **kwargs):
        return Book.objects.filter(author__pk=self.kwargs['pk'])


class category_books_list(ListView):
    model = Book
    context_object_name = 'category_books_list'
    template_name = 'FreeBooks/category_books_list.html'
    def get_queryset(self, **kwargs):
        return Book.objects.filter(category__pk=self.kwargs['pk'])

class user_profile(TemplateView):
    template_name = 'FreeBooks/user.html'
    model = Profile

    def get(self, request, **kwargs):
        current_user = self.request.user.id
        if (current_user is None):
            return redirect('FreeBooks:home')
        else:
            user = Profile.objects.get(user_id=current_user)
            return render(self.request, 'FreeBooks/user.html', {'profile': user, 'favourite_categories': user.favourite_category.all()})
