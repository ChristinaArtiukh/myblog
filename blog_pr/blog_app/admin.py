from django.contrib import admin
from .models import News, Category, CommentsAuthor, User, AuthorInfo, CommentsNews, Writer, \
    Book, Publisher, Genre, CommentsWriter, CommentsBook


# ------------USER--------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'author_status', 'i_am_author')
    ordering = ('-date_joined', )
    save_on_top = True


# ------------SHOP--------------
@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ('writer_name', 'slug')
    list_filter = ('writer_name', )
    search_fields = ('writer_name', 'content')
    prepopulated_fields = {'slug': ('writer_name',)}
    ordering = ('writer_name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher_name', 'status', 'maker', 'creation_date', 'update_date')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('creation_date', 'update_date')
    search_fields = ('title', 'content')
    ordering = ('-creation_date',)
    raw_id_fields = ('genre_name', 'publisher_name', 'writer')
    save_on_top = True


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('publisher_name', 'slug')
    list_filter = ('publisher_name',)
    search_fields = ('publisher_name', 'content')
    ordering = ('publisher_name',)
    prepopulated_fields = {'slug': ('publisher_name',)}


@admin.register(CommentsWriter)
class CommentsWriterAdmin(admin.ModelAdmin):
    list_display = ('author_name', )
    search_fields = ('writer', 'comment')
    ordering = ('-date',)


@admin.register(CommentsBook)
class CommentsBookAdmin(admin.ModelAdmin):
    list_display = ('author_name', )
    search_fields = ('book', 'comment')
    ordering = ('-date',)


admin.site.register(Genre)


# ------------BLOG--------------
@admin.register(AuthorInfo)
class AuthorInfoAdmin(admin.ModelAdmin):
    list_display = ('maker',)
    prepopulated_fields = {'slug': ('maker',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
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
