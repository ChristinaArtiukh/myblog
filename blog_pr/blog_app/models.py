from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse
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
    age = models.IntegerField(verbose_name='Возвраст', blank=True, default=0)
    preferences = models.ManyToManyField('Category', verbose_name='Предпочтения', blank=True)
    i_am_author = models.BooleanField(default=False, verbose_name='Я автор')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class AuthorActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active='active')


class Author(models.Model):
    ACTIVE_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    author_user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE, verbose_name='Информация автора')
    name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    about = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='media/%Y/%m/%d', blank=True, verbose_name='Фото')
    b_day = models.DateField(blank=True, verbose_name='День рождения')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    change_date = models.DateTimeField(auto_now=True, verbose_name='Дата внесения изменеий')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Ссылка')
    active = models.CharField(max_length=100, verbose_name='Активность', choices=ACTIVE_STATUS, default='inactive')
    number_of_news = models.IntegerField(verbose_name='Количество статей', blank=True, default=0)
    age = models.IntegerField(verbose_name='Возвраст', blank=True, default=0)
    number_days_of_activity = models.IntegerField(verbose_name='Количество дней активности', blank=True, default=0)
    objects = models.Manager()
    activity = AuthorActivityManager()

    class Meta:
        ordering = ['-reg_date']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author', args=[self.slug])

    def save(self, **kwargs):
        slug_str = "%s" % (self.author_user)
        unique_slugify(self, slug_str)
        super(Author, self).save(**kwargs)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class News(models.Model):
    PUBLICATION_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    author_user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель', default=1)
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(verbose_name='Контент')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    change_date = models.DateTimeField(auto_now=True, verbose_name='Дата внесения изменений')
    photo = models.ImageField(upload_to='media/%Y/%m/%d', blank=True, verbose_name='Фото')
    status = models.CharField(max_length=100, choices=PUBLICATION_STATUS, default='draft', verbose_name='Статус')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Ссылка')
    objects = models.Manager()
    published = PublishedManager()
    author = models.ForeignKey('Author', verbose_name='Автор', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    views = models.IntegerField(verbose_name='Количество просмотров', blank=True, default=0)
    comments = models.IntegerField(verbose_name='Количество комментариев', blank=True, default=0)
    liked = models.IntegerField(verbose_name='Количество лайков', blank=True, default=0)

    class Meta:
        ordering = ['-create_date', '-change_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news', args=[self.slug])


class Category(models.Model):
    author_user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель', default=1)
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Ссылка')
    number_of_news = models.IntegerField(verbose_name='Колличество статей', blank=True, default=0)
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
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        ordering = ['author_name']
        verbose_name = 'Комментарий к автору'
        verbose_name_plural = 'Комментарии к автору'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('add_comment', args=[self.pk])


class CommentsNews(models.Model):
    author_name = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель')
    comment = models.TextField(verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    news = models.ForeignKey('News', on_delete=models.CASCADE, verbose_name='Автор')


