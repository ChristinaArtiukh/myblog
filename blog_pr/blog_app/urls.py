from django.urls import path
from .views import HomeNewsViews, NewsDetailViews, UserPageView, AuthorListViews, AuthorDetailViews, \
    CategoryListViews, NewsListViews, CategoryDetailViews, user_logout, user_login, registration, AuthorPageView,\
    AuthorCreateView, AuthorUpdateView


urlpatterns = [
    path('', HomeNewsViews.as_view(), name='home'),
    path('news/', NewsListViews.as_view(), name='news_list'),
    path('news/<slug:slug>', NewsDetailViews.as_view(), name='news'),

    path('authors/', AuthorListViews.as_view(), name='authors'),
    path('author/<slug:slug>', AuthorDetailViews.as_view(), name='author'),
    path('author_profile/', AuthorPageView.as_view(), name='author_profile'),
    path('author_profile/create', AuthorCreateView.as_view(), name='author_create'),
    path('author_profile/update/<slug:slug>', AuthorUpdateView.as_view(), name='author_update'),

    path('categories/', CategoryListViews.as_view(), name='categories'),
    path('categories/<slug:slug>', CategoryDetailViews.as_view(), name='category'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('registration/', registration, name='registration'),
    path('user/', UserPageView.as_view(), name='user_info'),
]
