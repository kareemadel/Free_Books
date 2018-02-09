from django.contrib import admin
from .models import Author, Book, Category, Profile, Rate, Read, WishList

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Rate)
admin.site.register(Read)
admin.site.register(WishList)