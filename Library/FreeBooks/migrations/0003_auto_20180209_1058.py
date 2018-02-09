# Generated by Django 2.0.2 on 2018-02-09 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FreeBooks', '0002_auto_20180208_2353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='pic_url',
        ),
        migrations.RemoveField(
            model_name='book',
            name='pic_url',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='pic_url',
        ),
        migrations.AddField(
            model_name='author',
            name='pic',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Author Picture'),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to', to='FreeBooks.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='pic',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Book Cover'),
        ),
        migrations.AddField(
            model_name='profile',
            name='pic',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Profile Picture'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=50, verbose_name='User Name'),
        ),
    ]
