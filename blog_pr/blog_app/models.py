from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from django.contrib.auth.models import AbstractUser


# Managers:
class PublishedNewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class PublishedBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


# ------------USER--------------
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
        verbose_name_plural = 'USER-Пользователи'

    def __str__(self):
        return self.username

    def get_absolute_url_update(self):
        return reverse('profile', args=[self.slug])


# class UserBookListPreference(models.Model):
#     user = models.OneToOneField('User', verbose_name='Книги', blank=True)
#     book = models.ManyToManyField('Book', verbose_name='Книги', blank=True)
# ------------SHOP--------------
class Book(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    maker = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель')
    title = models.CharField(max_length=100, blank=True, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(max_length=100, blank=True, verbose_name='Ссылка')
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default='published', blank=True, verbose_name='Статус')
    number_of_pages = models.PositiveSmallIntegerField(blank=True, verbose_name='Количество страниц')
    publish_year = models.DateField(verbose_name='Год публикации', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Дата обновления')
    photo1 = models.ImageField(blank=True, upload_to='media/%Y/%m/%d', verbose_name='Фото1')
    photo2 = models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d', verbose_name='Фото2')
    price = models.PositiveSmallIntegerField(blank=True, verbose_name='Цена', default='1')
    discount = models.PositiveSmallIntegerField(blank=True, verbose_name='Скидка', default='1')
    writer = models.ForeignKey('Writer', blank=True, on_delete=models.CASCADE, verbose_name='Автор')
    publisher = models.ForeignKey('Publisher', blank=True, on_delete=models.CASCADE, verbose_name='Издательство')
    genre = models.ManyToManyField('Genre', blank=True, verbose_name='Жанр')
    objects = models.Manager()
    published = PublishedBookManager()

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'SHOP-Книги'
        ordering = ('-creation_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', args=[self.slug])


class Writer(models.Model):
    writer_name = models.CharField(max_length=100, blank=True, verbose_name='Имя автора')
    content = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(max_length=100, blank=True, verbose_name='Ссылка')
    photo1 = models.FileField(blank=True, upload_to='media/%Y/%m/%d', verbose_name='Фото1')
    photo2 = models.FileField(blank=True, upload_to='media/%Y/%m/%d', verbose_name='Фото2')

    def __str__(self):
        return self.writer_name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'SHOP-Авторы'
        ordering = ('writer_name',)

    def get_absolute_url(self):
        return reverse('writer', args=[self.slug])


class Publisher(models.Model):
    publisher_name = models.CharField(max_length=100, blank=True, verbose_name='Издательство')
    content = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(max_length=100, blank=True, verbose_name='Ссылка')
    photo1 = models.FileField(blank=True, upload_to='media/%Y/%m/%d', verbose_name='Фото1')

    def __str__(self):
        return self.publisher_name

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'SHOP-Издательства'
        ordering = ('publisher_name',)

    def get_absolute_url(self):
        return reverse('publisher', args=[self.slug])


class Genre(models.Model):
    genre_name = models.CharField(max_length=100, blank=True, verbose_name='Жанр')

    def __str__(self):
        return self.genre_name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'SHOP-Жанры'
        ordering = ('genre_name',)


class CommentsBook(models.Model):
    QUALITY = [
        ('1', 'Посредственно'),
        ('2', 'Неудовлетворительно'),
        ('3', 'Удовлетворительно'),
        ('4', 'Хорошо'),
        ('5', 'Отлично'),
    ]
    author_name = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель')
    comment = models.TextField(verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name='Книга')
    quality = models.CharField(max_length=100, choices=QUALITY, default='5', verbose_name='Оценка', blank=True)

    class Meta:
        ordering = ['author_name']
        verbose_name = 'Комментарий к книге'
        verbose_name_plural = 'SHOP-Комментарии к книге'

    def __str__(self):
        return self.comment


class CommentsWriter(models.Model):
    author_name = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name='Создатель')
    comment = models.TextField(verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    writer = models.ForeignKey('Writer', on_delete=models.CASCADE, verbose_name='Писатель')

    class Meta:
        ordering = ['author_name']
        verbose_name = 'Комментарий к писателю'
        verbose_name_plural = 'SHOP-Комментарии к писателю'

    def __str__(self):
        return self.comment


# ------------BLOG--------------
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
        verbose_name_plural = 'BLOG-Информация о авторах'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_info', args=[self.slug])

    def get_absolute_url_update(self):
        return reverse('update_author', args=[self.slug])

    def get_absolute_url_add_news(self):
        return reverse('add_news', args=[self.slug])

    def get_absolute_url_profile(self):
        return reverse('profile', args=[self.slug])

    def save_slug(self, *args, **kwargs):
        self.slug = slugify(self.maker)
        super().save(*args, **kwargs)


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
    published = PublishedNewsManager()
    author = models.ForeignKey('AuthorInfo', verbose_name='Автор', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-create_date', '-change_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'BLOG-Новости'

    def __str__(self):
        return self.title

    def get_absolute_url_update_news(self):
        return reverse('update_news', args=[self.slug])

    def get_absolute_url(self):
        return reverse('news', args=[self.slug])

    def get_absolute_url_delete_news(self):
        return reverse('delete_news', args=[self.slug])

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
        verbose_name_plural = 'BLOG-Категории'

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
        verbose_name_plural = 'BLOG-Комментарии к автору'

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
        verbose_name_plural = 'BLOG-Комментарии к статьям'

    def __str__(self):
        return self.comment
