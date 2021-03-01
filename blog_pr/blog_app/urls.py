from django.urls import path
from .views import HomeNewsViews, NewsDetailViews, ProfilePageView,\
    CategoryListViews, NewsListViews, CategoryDetailViews, user_logout, user_login, registration, \
    add_profile_info, AuthorListViews, AuthorDetailViews, UserUpdateView, AuthorUpdateView, AddNewsView, \
    NewsUpdateView


urlpatterns = [
    path('', HomeNewsViews.as_view(), name='home'),
    path('news/', NewsListViews.as_view(), name='news_list'),
    path('news/<slug:slug>', NewsDetailViews.as_view(), name='news'),

    path('authors/', AuthorListViews.as_view(), name='authors'),
    path('author/<slug:slug>', AuthorDetailViews.as_view(), name='author_info'),

    path('categories/', CategoryListViews.as_view(), name='categories'),
    path('categories/<slug:slug>', CategoryDetailViews.as_view(), name='category'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('registration/', registration, name='registration'),

    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('profile/create', add_profile_info, name='create_info'),
    path('profile/update', UserUpdateView.as_view(), name='update_info'),
    path('profile/update/<slug:slug>', AuthorUpdateView.as_view(), name='update_author'),
    # path('profile/add_news/', add_news, name='add_news'),
    path('profile/add_news/<slug:slug>', AddNewsView.as_view(), name='add_news'),
    path('profile/update_news/<slug:slug>', NewsUpdateView.as_view(), name='update_news'),

]
