from django.contrib import admin
from .models import News, Author, Category, CommentsAuthor, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name', 'last_name',)}


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
    list_display = ('author_name',)

