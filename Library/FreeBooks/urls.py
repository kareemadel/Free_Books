from django.urls import path, re_path
from .views import home_view, book_view, book_list_view, category_list_view, authorsListView, authorsDetailView, create_profile, Search , book_author_list,category_books_list, user_profile
from django.contrib.auth import views as auth_views

app_name = 'FreeBooks'

urlpatterns = [
    path('', home_view.as_view(), name='home'),
    path('book/<pk>', book_view.as_view(), name='book_detail'),
    path('books/', book_list_view.as_view(), name='book_list'),
    path('categories/', category_list_view.as_view(), name='category_list'),
    path('authors/', authorsListView.as_view(), name='AuthorList'),
    path('author/<int:pk>', authorsDetailView.as_view(), name='AuthorDetail'),
    path('register/', create_profile, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='FreeBooks/registration/login.html'), name='login'),
    path('profile/', user_profile.as_view(), name='user_profile'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    re_path(r'^search$', Search.as_view(), name='search_result'),
	path('books/<pk>', book_author_list.as_view(), name='book_author_list'),
	path('categoriesBooks/<pk>', category_books_list.as_view(), name='category_books_list'),

]
