from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import FormMixin
from .forms import AddCommentsAuthorForm, AddCommentsNewsForm, CreateAuthorForm, LoginUserForm, RegisteredUserForm,\
    UpdateAuthorForm
from .models import News, Author, Category, CommentsAuthor, CommentsNews, User
from django.contrib.auth import login, logout


class HomeNewsViews(ListView):
    model = News
    template_name = 'home_news_list.html'
    context_object_name = 'news'
    queryset = News.published.all()
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(HomeNewsViews, self).get_context_data(**kwargs)
        context['author_list'] = Author.activity.all()
        context['comments_count'] = CommentsNews.objects.annotate(comments_count=Count('pk')).values('news_id')
        return context


class NewsListViews(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = News.published.all()
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(NewsListViews, self).get_context_data(**kwargs)
        context['author_list'] = Author.activity.all()
        context['category'] = Category.objects.all()
        context['comments_count'] = CommentsNews.objects.annotate(comments_count=Count('pk')).values('news_id')
        return context


class NewsDetailViews(FormMixin, DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'
    form_class = AddCommentsNewsForm

    def get_context_data(self, **kwargs):
        context = super(NewsDetailViews, self).get_context_data(**kwargs)
        context['news'] = News.published.filter(category=self.object.category)
        context['prev_news'] = News.published.filter(category=self.object.category).filter(create_date__lt=self.object.create_date).filter(~Q(id=self.object.id))
        context['next_news'] = News.published.filter(category=self.object.category).filter(create_date__gt=self.object.create_date).filter(~Q(id=self.object.id))
        context['author_news'] = Author.activity.all()
        context['comments'] = CommentsNews.objects.all().values('name', 'date', 'comment').filter(news_id=self.object.pk).order_by('-date')
        context['comments_count'] = CommentsNews.objects.filter(news_id=self.object.pk).annotate(comments_count=Count('pk')).values_list('comments_count', flat=True)
        return context

    def add_news_comments(self, request,  *args, **kwargs):
        if request.method == 'POST':
            form = AddCommentsNewsForm(request.POST)
            if form.is_valid():
                this_news = News.objects.get(slug=self.kwargs['slug'])
                form = form.save(commit=False)
                form.news = this_news
                form.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                form = AddCommentsAuthorForm()
        return render(request, 'news_detail.html', {'form': form})


class AuthorListViews(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'author_list'
    queryset = Author.activity.all()
    paginate_by = 9


class AuthorDetailViews(FormMixin, DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author_detail'
    form_class = AddCommentsAuthorForm

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailViews, self).get_context_data(**kwargs)
        context['news'] = News.published.filter(author=self.object.pk)
        context['category'] = Category.objects.all()
        context['categories_unique'] = News.published.all().values('category','author_id').order_by('category').distinct()
        # context['comments'] = CommentsAuthor.objects.all().values('name', 'date', 'comment').filter(author_id=self.object.pk).order_by('-date')
        # context['comments_count'] = CommentsAuthor.objects.filter(author_id=self.object.pk).annotate(comments_count=Count('pk')).values_list('comments_count', flat=True)
        return context

    def add_author_comments(self, request,  *args, **kwargs):
        if request.method == 'POST':
            form = AddCommentsAuthorForm(request.POST)
            if form.is_valid():
                this_author = Author.objects.get(slug=self.kwargs['slug'])
                form = form.save(commit=False)
                form.author = this_author
                form.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                form = AddCommentsAuthorForm()
        return render(request, 'author_detail.html', {'form': form})


class UserPageView(ListView):
    model = User
    template_name = 'user_page.html'
    context_object_name = 'user_info'


class AuthorPageView(ListView):
    model = Author
    template_name = 'author_page.html'
    context_object_name = 'author_profile'


class AuthorCreateView(FormMixin, ListView):
    model = Author
    template_name = 'author_create_page.html'
    context_object_name = 'author_create'
    form_class = CreateAuthorForm

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CreateAuthorForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.author_user = request.user
                form.name = request.user.first_name
                form.last_name = request.user.last_name
                form.photo = request.FILES['photo']
                form.save()
                return redirect('author_profile')
        else:
            form = CreateAuthorForm()
        return render(request, 'author_create_page.html', {'form': form})


class AuthorUpdateView(UpdateView):
    model = Author
    template_name = 'author_update_page.html'
    form_class = UpdateAuthorForm
    success_url = reverse_lazy('author_profile')

    def update_author_info(self, request, *args, **kwargs):
        author_info = request.slug
        if request.method == 'POST':
            form = UpdateAuthorForm(request.POST, request.FILES, instance=author_info)
            if form.is_valid():
                form.save()
                return redirect('author_profile')
        else:
            form = CreateAuthorForm()
        return render(request, 'author_create_page.html', {'form': form})


class CategoryListViews(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()
    paginate_by = 10


class CategoryDetailViews(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailViews, self).get_context_data(**kwargs)
        context['news'] = News.published.filter(category=self.object.pk)
        context['author_list'] = Author.activity.all()
        return context


def registration(request):
    if request.method == 'POST':
        form = RegisteredUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успех')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegisteredUserForm()
    return render(request, 'registration.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginUserForm()
    return render(request, 'login.html', {'form': form})



