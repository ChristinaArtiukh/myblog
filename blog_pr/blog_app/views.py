from django.core import serializers
from django.db.models import Count, Max, Min, Avg
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from .filters import BookFilterSidebar
from .serializers import BookSerializer
from .forms import AddCommentsAuthorForm, AddCommentsNewsForm, LoginUserForm, RegisteredUserForm, CreateAuthorForm, \
    UserAddInfoForm, UpdateUserForm, UpdateAuthorForm, AddNewsForm, UpdateNewsForm, ChangeStatusNewsForm, \
    CommentsBookForm, CommentsWriterForm
from .models import News, Category, CommentsNews, User, AuthorInfo, CommentsAuthor, Book, Writer, Publisher,\
    Genre, CommentsBook, CommentsWriter, Order, OrderBook
from django.contrib.auth import login, logout



# Тест

# Фильтры

def is_valid_queryparam(param):
    return param != '' and param is not None


def blog_search(request):
    news_qs = News.published.all()
    search_qs = request.GET.get('search')
    if is_valid_queryparam(search_qs):
        news_qs = news_qs.filter(Q(title__icontains=search_qs) \
                                 | Q(content__icontains=search_qs))
    return news_qs


def shop_search(request):
    qs = Book.published.all()
    title_or_writer_query = request.GET.get('title_or_writer_query')

    if is_valid_queryparam(title_or_writer_query):
        qs = qs.filter(Q(title__icontains=title_or_writer_query) | Q(writer__writer_name__icontains=title_or_writer_query))
    return qs


#Home
class HomeViews(ListView):
    model = Book
    template_name = 'home_news_list.html'
    context_object_name = 'books'
    queryset = Book.published.all()
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(HomeViews, self).get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['author_list'] = AuthorInfo.objects.all()
        context['author_info'] = User.objects.filter(author_status='author')
        context['comments_count'] = News.published.values('pk').annotate(count=Count('comments')).filter(count__gt=0)
        context['news'] = News.published.all()
        return context


# ------------CART--------------

def list_book(request):
    context = {
        'catalog': Book.published.all()
    }
    return render(request, 'shop/cart/list_book.html', context)


# ------------SHOP--------------
class CatalogBookListView(FilterView, ListView):
    model = Book
    template_name = 'shop/book/catalog.html'
    context_object_name = 'catalog'
    paginate_by = 6
    filterset_class = BookFilterSidebar


    def get_context_data(self, **kwargs):
        context = super(CatalogBookListView, self).get_context_data()
        context['title'] = 'Каталог'
        context['writer'] = Writer.objects.all()
        context['publisher'] = Publisher.objects.all()
        context['genre'] = Genre.objects.all()
        context['genre_count'] = Genre.objects.annotate(count=Count('book')).filter(count__gt=0)
        context['writer_count'] = Writer.objects.annotate(count=Count('book')).filter(count__gt=0)
        context['publisher_count'] = Publisher.objects.annotate(count=Count('book')).filter(count__gt=0)
        context['high_price'] = Book.published.all().values('price',).aggregate(max=Max('price'))
        context['low_price'] = Book.published.all().values('price',).aggregate(min=Min('price'))

        context['ordering_low_price'] = Book.published.all().values('price').order_by('price').distinct()
        context['ordering_high_price'] = Book.published.all().values('price').order_by('-price').distinct()
        context['ordering_id'] = Book.published.all().values('id').order_by('-id').distinct()

        context['publisher_filter'] = Book.published.all().values('publisher__publisher_name').order_by('publisher__publisher_name').distinct()
        context['writer_filter'] = Book.published.all().values('writer__writer_name').order_by('writer__writer_name').distinct()
        context['genre_filter'] = Book.published.all().values('genre__genre_name').order_by('genre__genre_name').distinct()
        return context

    def get_queryset(self):
        qs = shop_search(self.request)
        return qs

class BookDetailView(DetailView):
    model = Book
    template_name = 'shop/book/book.html'
    context_object_name = 'book'
    form_class = CommentsBookForm

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data()
        context['writer'] = Writer.objects.filter(pk=self.object.writer_id)
        context['publisher'] = Publisher.objects.filter(pk=self.object.publisher_id)
        context['genre_all'] = Genre.objects.all()
        context['user'] = User.objects.all()
        context['comments'] = CommentsBook.objects.filter(book=self.object.pk)
        context['avg'] = CommentsBook.objects.filter(book=self.object.pk).values('quality',).aggregate(avg=Avg('quality'))
        context['quality_count'] = Book.objects.filter(pk=self.object.pk).values('pk',).annotate(count=Count('commentsbook')).filter(count__gt=0)
        return context

    def post(self, request, **kwargs):
        if request.method == 'POST':
            form = CommentsBookForm(request.POST)
            if form.is_valid():
                this_book = Book.objects.get(slug=self.kwargs['slug'])
                form = form.save(commit=False)
                form.author_name = self.request.user
                form.book = this_book
                form.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                form = CommentsBookForm()
        return render(request, 'shop/book/book.html', {'form': form})


class WritersListView(ListView):
    model = Writer
    context_object_name = 'writers'
    template_name = 'shop/writer/writers.html'
    queryset = Writer.objects.all()
    paginate_by = 20


class WriterDetailView(FormMixin, DetailView):
    model = Writer
    context_object_name = 'writer'
    template_name = 'shop/writer/writer.html'
    form_class = CommentsWriterForm


class PublishersListView(ListView):
    model = Publisher
    context_object_name = 'publishers'
    template_name = 'shop/publisher/publishers.html'
    queryset = Publisher.objects.all()
    paginate_by = 20


class PublisherDetailView(DetailView):
    model = Publisher
    context_object_name = 'publisher'
    template_name = 'shop/publisher/publisher.html'


# ------------BLOG--------------
# News list
class NewsListViews(ListView):
    model = News
    template_name = 'blog/news/news.html'
    context_object_name = 'news'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(NewsListViews, self).get_context_data(**kwargs)
        context['title'] = 'Список новостей'
        context['author_list'] = AuthorInfo.objects.all()
        context['author_info'] = User.objects.filter(author_status='author')
        context['category'] = Category.objects.all()
        context['comments_count'] = News.published.values('pk').annotate(count=Count('comments')).filter(count__gt=0)
        context['category_count'] = Category.objects.annotate(count=Count('news')).filter(count__gt=0)
        return context

    def get_queryset(self):
        # news_qs = News.published.all()
        news_qs = blog_search(self.request)
        return news_qs


# News detail
class NewsDetailViews(FormMixin, DetailView):
    model = News
    template_name = 'blog/news/news_detail.html'
    context_object_name = 'news_detail'
    form_class = AddCommentsNewsForm

    def get_context_data(self, **kwargs):
        context = super(NewsDetailViews, self).get_context_data(**kwargs)
        context['news'] = News.published.filter(category=self.object.category)
        context['prev_news'] = News.published.filter(category=self.object.category,
                                                     ).filter(create_date__lt=self.object.create_date,
                                                              ).filter(~Q(id=self.object.id))
        context['next_news'] = News.published.filter(category=self.object.category,
                                                     ).filter(create_date__gt=self.object.create_date,
                                                              ).filter(~Q(id=self.object.id))
        context['user_news'] = User.objects.filter(author_status='author', pk=self.object.maker_id)
        context['users_all'] = User.objects.all()
        context['author_news'] = AuthorInfo.objects.all()
        context['comments'] = CommentsNews.objects.all().values('comment',
                                                                'author_name',
                                                                'date').filter(news_id=self.object.pk).order_by('-date')
        context['comments_count'] = CommentsNews.objects.filter(news_id=self.object.pk,
                                                                ).annotate(comments_count=Count('pk'),
                                                                           ).values_list('comments_count', flat=True)
        return context

    def post(self, request,  *args, **kwargs):
        if request.method == 'POST':
            form = AddCommentsNewsForm(request.POST)
            if form.is_valid():
                this_news = News.objects.get(slug=self.kwargs['slug'])
                form = form.save(commit=False)
                form.news = this_news
                form.author_name = request.user
                form.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                form = AddCommentsNewsForm()
        return render(request, 'news_detail.html', {'form': form})


# Authors list
class AuthorsListViews(ListView):
    model = User
    template_name = 'blog/author/authors.html'
    context_object_name = 'author_info'
    queryset = User.objects.filter(author_status='author')
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(AuthorsListViews, self).get_context_data(**kwargs)
        context['title'] = 'Список авторов'
        context['slug'] = AuthorInfo.objects.all()
        return context


# Author detail
class AuthorDetailViews(FormMixin, DetailView):
    model = AuthorInfo
    template_name = 'blog/author/author_detail.html'
    context_object_name = 'author_info'
    form_class = AddCommentsAuthorForm

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailViews, self).get_context_data(**kwargs)
        context['author_detail'] = User.objects.filter(author_status='author', pk=self.object.maker_id)
        context['user_all'] = User.objects.all()
        context['news'] = News.published.filter(author=self.object.pk)
        context['categories_unique'] = News.published.all().values('category','author_id').order_by('category').distinct()
        context['category_count'] = Category.objects.all().annotate(count=Count('news')).filter(count__gt=0)
        context['comments'] = CommentsAuthor.objects.all().values('author_name', 'date', 'comment',
                                                                  ).filter(author_id=self.object.pk).order_by('-date')
        context['comments_count'] = CommentsAuthor.objects.filter(author_id=self.object.pk,
                                                                  ).annotate(comments_count=Count('pk',
                                                                )).values_list('comments_count', flat=True)
        return context

    def post(self, request,  *args, **kwargs):
        if request.method == 'POST':
            form = AddCommentsAuthorForm(request.POST)
            if form.is_valid():
                this_author = AuthorInfo.objects.get(slug=self.kwargs['slug'])
                form = form.save(commit=False)
                form.author = this_author
                form.author_name = request.user
                form.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                form = AddCommentsAuthorForm()
        return render(request, 'author_detail.html', {'form': form})


# Category list
class CategoriesListViews(ListView):
    model = Category
    template_name = 'blog/category/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(CategoriesListViews, self).get_context_data(**kwargs)
        context['title'] = 'Список категорий'
        return context


# Category detail
class CategoryDetailViews(DetailView):
    model = Category
    template_name = 'blog/category/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailViews, self).get_context_data(**kwargs)
        context['news'] = News.published.filter(category=self.object.pk)
        context['user_list'] = User.objects.filter(author_status='author')
        context['author_list'] = AuthorInfo.objects.all()
        context['comments_count'] = News.published.values('pk').annotate(count=Count('comments')).filter(count__gt=0)
        return context


# --------------USER-------------
# Registration
def registration(request):
    if request.method == 'POST':
        form = RegisteredUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_info')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegisteredUserForm()
    return render(request, 'user/registration.html', {'form': form})


# Login
def user_login(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginUserForm()
    return render(request, 'user/login.html', {'form': form})


# Logout
def user_logout(request):
    logout(request)
    return redirect('login')


# Profile
class ProfilePageView(ListView):
    model = AuthorInfo
    template_name = 'user/profile_page.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(ProfilePageView, self).get_context_data(**kwargs)
        context['news_list'] = News.published.all()
        context['author'] = AuthorInfo.objects.all()
        return context


# add info for new user
def add_profile_info(request):
    if request.user.i_am_author == True:
        user_info = request.user
        if request.method == 'POST':
            form_one = UserAddInfoForm(request.POST, request.FILES, instance=user_info)
            form = CreateAuthorForm(request.POST)
            if form.is_valid() and form_one.is_valid():
                form_one.save(commit=False)
                form_one.photo = request.FILES['photo']
                form_one.save()
                form = form.save(commit=False)
                form.maker = request.user
                form.name = request.user.first_name
                form.save_slug()
                return redirect('profile')
        else:
            form = CreateAuthorForm()
            form_one = UserAddInfoForm()
        return render(request, 'user/create_info_page.html', {'form': form, 'form_one': form_one})
    else:
        user_info = request.user
        if request.method == 'POST':
            form_one = UserAddInfoForm(request.POST, request.FILES, instance=user_info)
            if form_one.is_valid():
                form_one.save(commit=False)
                form_one.photo = request.FILES['photo']
                form_one.save()
                return redirect('profile')
        else:
            form_one = UserAddInfoForm()
        return render(request, 'user/create_info_page.html', {'form_one': form_one})


# Update user info
class UserUpdateView(UpdateView):
    model = User
    template_name = 'user/update_info_page.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


# Update author info
class AuthorUpdateView(UpdateView):
    model = AuthorInfo
    template_name = 'user/author/author_update_page.html'
    form_class = UpdateAuthorForm
    success_url = reverse_lazy('update_info')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


# Add news only for user with author status
class AddNewsView(FormMixin, DetailView):
    model = AuthorInfo
    template_name = 'user/author/add_news.html'
    context_object_name = 'add_news'
    form_class = AddNewsForm

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = AddNewsForm(request.POST, request.FILES)
            if form.is_valid():
                this_author = AuthorInfo.objects.get(slug=self.kwargs['slug'])
                form = form.save(commit=False)
                form.author = this_author
                form.maker = request.user
                form.photo = request.FILES['photo']
                form.save_news()
                return redirect('profile')
        else:
            form = AddNewsForm()
        return render(request, 'user/author/add_news.html', {'form': form})


# Update news only for user with author status
class NewsUpdateView(UpdateView):
    model = News
    template_name = 'user/author/news_update_page.html'
    form_class = UpdateNewsForm
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        # view_name = имя модели
        view_name = 'news'
        return reverse(view_name, kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


# Change news status
class ChangeStatusNewsView(UpdateView):
    model = News
    template_name = 'user/author/change_status_news.html'
    form_class = ChangeStatusNewsForm
    queryset = News.published.all()
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'draft'
        self.object.save(update_fields=('status',))
        return redirect('profile')












