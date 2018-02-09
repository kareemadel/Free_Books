from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Author(models.Model):

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    author_id = models.AutoField("Author ID", primary_key=True)
    birth_date = models.DateField("Date of Birth", null=True, blank=True)
    death_date = models.DateField("Date of Death", null=True, blank=True)
    pic = models.ImageField("Author Picture", blank=True)
    name = models.CharField("Author name", max_length=50)
    bio = models.TextField("Bio", blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    book_id = models.AutoField("Book ID", primary_key=True)
    author_id = models.ForeignKey(Author, related_name="Write", on_delete=models.CASCADE)
    publish_date = models.DateField("Published at", null=True, blank=True)
    summary = models.TextField("Summary", blank=True)
    country = models.CharField("Country", max_length=50, blank=True)
    link = models.URLField("Link", blank=True)
    name = models.CharField("Book Name", max_length=50)
    pic = models.ImageField("Book Cover", blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    category_id = models.AutoField("Category_id", primary_key=True)
    name = models.CharField("Category Name", max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField("User Name", blank=True, max_length=50)
    email = models.EmailField("Email", blank=True, max_length=50)
    birth_date = models.DateField("Date of Birth", null=True, blank=True)
    pic = models.ImageField("Profile Picture", blank=True)
    name = models.CharField("User Name", max_length=50)
    favourite_category = models.ForeignKey(Category, related_name="favorite_category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Rate(models.Model):

    class Meta:
        verbose_name = "Rate"
        verbose_name_plural = "Rates"
        unique_together = (('user_id', 'book_id'),)

    rate_id = models.AutoField("Read ID", primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    def __str__(self):
        pass
    


class Read(models.Model):

    class Meta:
        verbose_name = "Read"
        verbose_name_plural = "Reads"
        unique_together = (('user_id', 'book_id'),)

    read_id = models.AutoField("Read ID", primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.read_id


class WishList(models.Model):

    class Meta:
        verbose_name = "WishList"
        verbose_name_plural = "WishLists"
        unique_together = (('user_id', 'book_id'),)

    wish_id = models.AutoField("Read ID", primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        pass
