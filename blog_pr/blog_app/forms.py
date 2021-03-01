from django import forms
from django.http import request
from .models import News, CommentsAuthor, CommentsNews, User, AuthorInfo
from django.utils.translation import gettext_lazy as gl
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class AddCommentsAuthorForm(forms.ModelForm):
    class Meta:
        model = CommentsAuthor
        fields = ('comment', )
        exclude = ['author_name', 'author']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 100, 'rows': 20, 'class': "form-control"}),
        }


class AddCommentsNewsForm(forms.ModelForm):
    class Meta:
        model = CommentsNews
        fields = ('comment', )
        exclude = ['author_name', 'news', 'name']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 100, 'rows': 20, 'class': "form-control"}),
        }


class UserAddInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('b_day', 'photo')
        exclude = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'photo': gl('Фото'),
            'b_day': gl('День рождения'),
        }
        widgets = {
            'about': forms.Textarea(attrs={'cols': 50, 'rows': 10 }),
        }


class CreateAuthorForm(forms.ModelForm):
    class Meta:
        model = AuthorInfo
        fields = ('about',)
        exclude = ('slug', 'name', 'maker')
        labels = {
            'about': gl('О вас'),
        }
        widgets = {
            'about': forms.Textarea(attrs={'cols': 50, 'rows': 10 }),
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'b_day', 'photo')


class UpdateAuthorForm(forms.ModelForm):
    class Meta:
        model = AuthorInfo
        fields = ('about',)
        exclude = ('maker',)
        widgets = {
            'about': forms.Textarea(attrs={'cols': 80, 'rows': 10 }),
        }


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class RegisteredUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'i_am_author')
        labels = {
            'username': gl('Логин'),
            'first_name': gl('Имя'),
            'last_name': gl('Фамилия'),
            'email': gl('Почта'),
            'password1': gl('Пароль'),
            'password2': gl('Подтверждение пароля'),
        }
        help_texts = {
            'username': gl('Введите логин'),
            'email': gl('Введите почту'),
            'password1': gl('Введите пароль'),
            'password2': gl('Введите пароль'),
        }


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'photo', 'category', 'content')
        exclude = ('maker', 'status', 'slug', 'author')
        labels = {
            'title': gl('Название'),
            'content': gl('Контент'),
            'photo': gl('Фото'),
            'category': gl('Категория'),
        }
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 10 }),
        }


class UpdateNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'photo', 'category', 'content')
        exclude = ('maker', 'status', 'slug', 'author')
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 10 }),
    }

# class AddNewsForm(forms.ModelForm):
#     class Meta:
#         model = News
#         fields = '__all__'
#             # ['title', 'author',  'category', 'status', 'content']
#         # field_classes = {
#         #     'slug': MySlugFormField,
#         # }
#         # widgets = {
#         #     'content': forms.Textarea(attrs={'cols': 80, 'rows': 20,}),
#         # }
#
#         labels = {
#             'title': gl('Название'),
#             'author': gl('Автор'),
#             'category': gl('Категория'),
#             'status': gl('Статус'),
#             'content': gl('Статья'),
#         }
#         help_texts = {
#             'title': gl('Введите название статьи'),
#             'author': gl('Выбирите имя автора'),
#             'category': gl('Выбирите категорию'),
#             'status': gl('Укажите статус'),
#             'content': gl('Добавьте статью'),
#         }
#         error_messages = {
#             'title': {
#                 'max_length': gl("Название статьи превышает лимит"),
#             },
#         }
