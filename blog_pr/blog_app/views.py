from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import FormMixin
from .forms import AddCommentsAuthorForm, AddCommentsNewsForm, LoginUserForm, RegisteredUserForm, CreateAuthorForm, \
    UserAddInfoForm, UpdateUserForm, UpdateAuthorForm, AddNewsForm, UpdateNewsForm
from .models import News, Category, CommentsNews, User, AuthorInfo, CommentsAuthor
from django.contrib.auth import login, logout


class HomeNewsViews(ListView):
    model = News
    template_name = 'home_news_list.html'
    context_object_name = 'news'
    queryset = News.published.all()
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(HomeNewsViews, self).get_context_data(**kwargs)
        context['author_list'] = AuthorInfo.objects.all()
        context['author_info'] = User.objects.filter(author_status='author')
        context['comments_count'] = News.published.values('pk').annotate(count=Count('comments')).filter(count__gt=0)
        return context


class NewsListViews(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = News.published.all()
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(NewsListViews, self).get_context_data(**kwargs)
        context['author_list'] = AuthorInfo.objects.all()
        context['author_info'] = User.objects.filter(author_status='author')
        context['category'] = Category.objects.all()
        context['comments_count'] = News.published.values('pk').annotate(count=Count('comments')).filter(count__gt=0)
        context['category_count'] = Category.objects.annotate(count=Count('news')).filter(count__gt=0)

        return context


class NewsDetailViews(FormMixin, DetailView):
    model = News
    template_name = 'news_detail.html'
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
        context['user_news'] = User.objects.filter(author_status='author')
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


class AuthorListViews(ListView):
    model = AuthorInfo
    template_name = 'authors.html'
    context_object_name = 'author_info'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(AuthorListViews, self).get_context_data(**kwargs)
        context['author_list'] = User.objects.filter(author_status='author')
        return context


class AuthorDetailViews(FormMixin, DetailView):
    model = AuthorInfo
    template_name = 'author_detail.html'
    context_object_name = 'author_info'
    form_class = AddCommentsAuthorForm

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailViews, self).get_context_data(**kwargs)
        context['author_detail'] = User.objects.filter(author_status='author')
        context['user_all'] = User.objects.all()
        context['news'] = News.published.filter(author=self.object.pk)
        context['categories_unique'] = News.published.all().values('category','author_id').order_by('category').distinct()
        context['category_count'] = Category.objects.all().annotate(count=Count('news')).filter(count__gt=0)
        context['comments'] = CommentsAuthor.objects.all().values('author_name', 'date', 'comment',
                                                                  ).filter(author_id=self.object.pk).order_by('-date')
        context['comments_count'] = CommentsAuthor.objects.filter(author_id=self.object.pk,
                                                                  ).annotate(comments_count=Count('pk',\
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


class ProfilePageView(ListView):
    model = AuthorInfo
    template_name = 'profile_page.html'
    context_object_name = 'profile'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(ProfilePageView, self).get_context_data(**kwargs)
        context['news_list'] = News.published.all()
        return context


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
        return render(request, 'create_info_page.html', {'form': form, 'form_one': form_one})
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
        return render(request, 'create_info_page.html', {'form_one': form_one})


class UserUpdateView(UpdateView):
    model = User
    template_name = 'update_info_page.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class AuthorUpdateView(UpdateView):
    model = AuthorInfo
    template_name = 'author_update_page.html'
    form_class = UpdateAuthorForm

    # def get_success_url(self):
    #     view_name = 'update_mymodel'
    #     return reverse(view_name, kwargs={'model_name_slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class AddNewsView(FormMixin, DetailView):
    model = AuthorInfo
    template_name = 'add_news.html'
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
        return render(request, 'add_news.html', {'form': form})


class NewsUpdateView(UpdateView):
    model = News
    template_name = 'news_update_page.html'
    form_class = UpdateNewsForm
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class CategoryListViews(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()
    paginate_by = 9


class CategoryDetailViews(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailViews, self).get_context_data(**kwargs)
        context['news'] = News.published.filter(category=self.object.pk)
        context['user_list'] = User.objects.filter(author_status='author')
        context['author_list'] = AuthorInfo.objects.all()
        context['comments_count'] = News.published.values('pk').annotate(count=Count('comments')).filter(count__gt=0)
        return context


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



