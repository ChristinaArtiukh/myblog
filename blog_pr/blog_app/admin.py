from django.contrib import admin
from .models import News, Category, CommentsAuthor, User, AuthorInfo, CommentsNews


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(AuthorInfo)
class AuthorInfoAdmin(admin.ModelAdmin):
    list_display = ('maker',)
    prepopulated_fields = {'slug': ('maker',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CommentsAuthor)
class CommentsAuthorAdmin(admin.ModelAdmin):
    list_display = ('comment',)


@admin.register(CommentsNews)
class CommentsNewsAdmin(admin.ModelAdmin):
    list_display = ('comment',)
