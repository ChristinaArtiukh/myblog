from django.urls import path
from .views import HomeViews, NewsDetailViews, ProfilePageView, \
    CategoriesListViews, NewsListViews, CategoryDetailViews, user_logout, user_login, registration, \
    add_profile_info, AuthorsListViews, AuthorDetailViews, UserUpdateView, AuthorUpdateView, AddNewsView, \
    NewsUpdateView, ChangeStatusNewsView, CatalogBookListView, PublishersListView, PublisherDetailView, \
    WritersListView, WriterDetailView, BookDetailView


urlpatterns = [
    path('', HomeViews.as_view(), name='home'),
    path('news/', NewsListViews.as_view(), name='news_list'),
    path('news/<slug:slug>', NewsDetailViews.as_view(), name='news'),

    path('authors/', AuthorsListViews.as_view(), name='authors'),
    path('author/<slug:slug>', AuthorDetailViews.as_view(), name='author_info'),

    path('categories/', CategoriesListViews.as_view(), name='categories'),
    path('categories/<slug:slug>', CategoryDetailViews.as_view(), name='category'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('registration/', registration, name='registration'),

    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('profile/create', add_profile_info, name='create_info'),
    path('profile/update', UserUpdateView.as_view(), name='update_info'),
    path('profile/update/<slug:slug>', AuthorUpdateView.as_view(), name='update_author'),
    path('profile/add_news/<slug:slug>', AddNewsView.as_view(), name='add_news'),
    path('profile/update_news/<slug:slug>', NewsUpdateView.as_view(), name='update_news'),
    path('profile/delete_news/<slug:slug>', ChangeStatusNewsView.as_view(), name='delete_news'),

    path('shop/', CatalogBookListView.as_view(), name='catalog'),
    path('book/<slug:slug>', BookDetailView.as_view(), name='book'),
    path('writers/', WritersListView.as_view(), name='writers'),
    path('writer/<slug:slug>', WriterDetailView.as_view(), name='writer'),
    path('publishers/', PublishersListView.as_view(), name='publishers'),
    path('publisher/<slug:slug>', PublisherDetailView.as_view(), name='publisher'),



]
