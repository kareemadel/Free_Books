from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, ListView
from .models import Book, Category, Author, Profile, Read, Rate, WishList, Follower
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class home_view(TemplateView):
    def get(self, request):
        return render(request, 'FreeBooks/HomePage.html')


class book_view(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id
        book = self.kwargs['pk']

        user = Profile.objects.filter(user_id=current_user)
        user = len(user) and user[0]

        read = Read.objects.filter(user_id=current_user, book_id=book)
        read = len(read) and read[0]

        rate = Rate.objects.filter(user_id=current_user, book_id=book)
        rate = len(rate) and rate[0].score
        rate_list = []
        rate_title = ('Poor', 'Fair', 'Good', 'Excellent', 'WOW!!!')
        for i in range(rate):
            rate_list.append(('star selected', rate_title[i], i + 1))
        for j in range(5 - rate):
            rate_list.append(('star', rate_title[j + rate], j + rate + 1))

        wish = WishList.objects.filter(user_id=current_user, book_id=book)
        wish = len(wish) and wish[0]

        context.update({
            'read': read,
            'wish': wish,
            'rate': rate_list,
        })
        return context

    def post(self, request, **kwargs):
        body = json.loads(self.request.body.decode("utf-8"))
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
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id

        user = Profile.objects.filter(user_id=current_user)
        user = len(user) and user[0]
        if user:
            reads = user.reading.all()
            wishes = user.wish.all()
            rates = user.rating.all()
        for book in context['book_list']:
            book.read = user and book in reads
            book.wish = user and book in wishes
            rate = user and Rate.objects.filter(user_id=current_user, book_id=book)
            rate = bool(rate) and len(rate) and rate[0].score
            book.rate = []
            rate_title = ('Poor', 'Fair', 'Good', 'Excellent', 'WOW!!!')
            for i in range(rate):
                book.rate.append(('star selected', rate_title[i], i + 1))
            for j in range(5 - rate):
                book.rate.append(('star', rate_title[j + rate], j + rate + 1))
        return context

class category_list_view(ListView):
    model = Category
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id

        user = Profile.objects.filter(user_id=current_user)
        user = len(user) and user[0]
        if user:
            categories = user.favourite_category.all()
        else:
            categories = Category.objects.all()
        for category in context['category_list']:
            category.favourite = user and category in categories
        return context

class authorsListView(ListView):
    model=Author
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id

        user = Profile.objects.filter(user_id=current_user)
        user = len(user) and user[0]
        if user:
            authors = user.follows.all()
        else:
            authors = Author.objects.all()
        for author in context['author_list']:
            author.followed = user and author in authors
        return context

class authorsDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id
        author = self.kwargs['pk']

        user = Profile.objects.filter(user_id=current_user)
        user = len(user) and user[0]

        follows = Follower.objects.filter(user_id=current_user, author_id=author)
        follows = len(follows) and follows[0]

        context.update({
            'follow': follows
        })
        return context

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
            messages.success(request, ('You have registered successfully!'))
            return redirect('FreeBooks:login')
        else:
            email = request.POST['email']
            username = request.POST['username']
            isEmail = bool(User.objects.filter(email=email))
            print(user_form.errors)
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
        page1q = self.request.GET.get('page1', '')
        page2q = self.request.GET.get('page2', '')
        querystring = {'q': q, 'page1': page1q, 'page2':page2q}
        context = super().get_context_data(**kwargs)
        book_list = Book.objects.filter(title__icontains=q)
        paginator = Paginator(book_list, 2)
        page1 = self.request.GET.get('page1')
        try:
            book_list = paginator.page(page1)
        except PageNotAnInteger:
            book_list = paginator.page(1)
        except EmptyPage:
            book_list = paginator.page(paginator.num_pages)

        author_list = Author.objects.filter(name__icontains=q)
        paginator = Paginator(author_list, 2)
        page2 = self.request.GET.get('page2')
        try:
            author_list = paginator.page(page2)
        except PageNotAnInteger:
            author_list = paginator.page(1)
        except EmptyPage:
            author_list = paginator.page(paginator.num_pages)


        current_user = self.request.user.id
        user = Profile.objects.filter(user_id=current_user)
        user = len(user) and user[0]
        if user:
            reads = user.reading.all()
            wishes = user.wish.all()
            rates = user.rating.all()
        for book in book_list:
            book.read = user and book in reads
            book.wish = user and book in wishes
            rate = user and Rate.objects.filter(user_id=current_user, book_id=book)
            rate = bool(rate) and len(rate) and rate[0].score
            book.rate = []
            rate_title = ('Poor', 'Fair', 'Good', 'Excellent', 'WOW!!!')
            for i in range(rate):
                book.rate.append(('star selected', rate_title[i], i + 1))
            for j in range(5 - rate):
                book.rate.append(('star', rate_title[j + rate], j + rate + 1))
        context.update({
            'book_list': book_list,
            'author_list': author_list,
            'q': querystring,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id

        user = Profile.objects.filter(user_id=current_user)
        user = len(user) and user[0]
        if user:
            reads = user.reading.all()
            wishes = user.wish.all()
            rates = user.rating.all()
        for book in context['book_author_list']:
            book.read = user and book in reads
            book.wish = user and book in wishes
            rate = user and Rate.objects.filter(user_id=current_user, book_id=book)
            rate = bool(rate) and len(rate) and rate[0].score
            book.rate = []
            rate_title = ('Poor', 'Fair', 'Good', 'Excellent', 'WOW!!!')
            for i in range(rate):
                book.rate.append(('star selected', rate_title[i], i + 1))
            for j in range(5 - rate):
                book.rate.append(('star', rate_title[j + rate], j + rate + 1))
        return context


class category_books_list(ListView):
    model = Book
    context_object_name = 'category_books_list'
    template_name = 'FreeBooks/category_books_list.html'
    def get_queryset(self, **kwargs):
        return Book.objects.filter(category__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id

        user = Profile.objects.filter(user_id=current_user)
        user = len(user) and user[0]
        if user:
            reads = user.reading.all()
            wishes = user.wish.all()
            rates = user.rating.all()
        for book in context['category_books_list']:
            book.read = user and book in reads
            book.wish = user and book in wishes
            rate = user and Rate.objects.filter(user_id=current_user, book_id=book)
            rate = bool(rate) and len(rate) and rate[0].score
            book.rate = []
            rate_title = ('Poor', 'Fair', 'Good', 'Excellent', 'WOW!!!')
            for i in range(rate):
                book.rate.append(('star selected', rate_title[i], i + 1))
            for j in range(5 - rate):
                book.rate.append(('star', rate_title[j + rate], j + rate + 1))
        return context

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
