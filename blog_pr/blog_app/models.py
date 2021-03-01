from django.core.files.storage import FileSystemStorage
from django.db import models
from django.shortcuts import render
from django.urls import reverse
from pytils.translit import slugify
from django_unique_slugify import unique_slugify
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    AUTHOR_STATUS = [
        ('author', 'Active'),
        ('inactive', 'Inactive')
    ]
    photo = models.ImageField(upload_to='media/%Y/%m/%d', blank=True, verbose_name='Фото')
    b_day = models.DateField(blank=True, verbose_name='День рождения', default='9999-01-01')
    author_status = models.CharField(max_length=100, verbose_name='Статус автора', choices=AUTHOR_STATUS, default='inactive')
    preferences = models.ManyToManyField('Category', verbose_name='Предпочтения', blank=True)
    i_am_author = models.BooleanField(default=False, verbose_name='Я автор')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_absolute_url_update(self):
        return reverse('profile', args=[self.slug])


class AuthorInfo(models.Model):
    maker = models.OneToOneField(User, blank=True, on_delete=models.CASCADE, verbose_name='Информация автора')
    name = models.CharField(max_length=150, verbose_name='Имя', blank=True)
    about = models.TextField(blank=True, verbose_name='Описание')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    change_date = models.DateTimeField(auto_now=True, verbose_name='Дата внесения изменеий')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Ссылка')

    class Meta:
        ordering = ['-reg_date']
        verbose_name = 'Информация о авторе'
        verbose_name_plural = 'Информация о авторах'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_info', args=[self.slug])

    def get_absolute_url_update(self):
        return reverse('update_author', args=[self.slug])

    def get_absolute_url_add_news(self):
        return reverse('add_news', args=[self.slug])

    def save_slug(self, *args, **kwargs):
        self.slug = slugify(self.maker)
        super().save(*args, **kwargs)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class News(models.Model):
    PUBLICATION_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    maker = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель', default=1)
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(verbose_name='Контент')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    change_date = models.DateTimeField(auto_now=True, verbose_name='Дата внесения изменений')
    photo = models.ImageField(upload_to='media/%Y/%m/%d', blank=True, verbose_name='Фото')
    status = models.CharField(max_length=100, choices=PUBLICATION_STATUS, default='published', verbose_name='Статус')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Ссылка')
    objects = models.Manager()
    published = PublishedManager()
    author = models.ForeignKey('AuthorInfo', verbose_name='Автор', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-create_date', '-change_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def get_absolute_url_update_news(self):
        return reverse('update_news', args=[self.slug])

    def get_absolute_url(self):
        return reverse('news', args=[self.slug])

    def save_news(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Category(models.Model):
    maker = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель')
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Ссылка')
    photo = models.ImageField(upload_to='media/%Y/%m/%d', blank=True, verbose_name='Фото')

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])


class CommentsAuthor(models.Model):
    author_name = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель')
    comment = models.TextField(verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey('AuthorInfo', on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        ordering = ['author_name']
        verbose_name = 'Комментарий к автору'
        verbose_name_plural = 'Комментарии к автору'

    def __str__(self):
        return self.comment


class CommentsNews(models.Model):
    author_name = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель')
    comment = models.TextField(verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    news = models.ForeignKey('News', related_name='comments', on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        ordering = ['author_name']
        verbose_name = 'Комментарий к статье'
        verbose_name_plural = 'Комментарии к статьям'

    def __str__(self):
        return self.comment
