from django import forms
from django.http import request
from .models import News, CommentsAuthor, CommentsNews, Author, User
from django.utils.translation import gettext_lazy as gl
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class AddCommentsAuthorForm(forms.ModelForm):
    class Meta:
        model = CommentsAuthor
        fields = ('author_name',  'comment')
        exclude = ['author']
        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control"}),
            'email': forms.TextInput(attrs={'class': "form-control"}),
            'comment': forms.Textarea(attrs={'cols': 100, 'rows': 20, 'class': "form-control"}),
        }


class AddCommentsNewsForm(forms.ModelForm):
    class Meta:
        model = CommentsNews
        fields = ('author_name', 'comment')
        exclude = ['news']
        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control"}),
            'email': forms.TextInput(attrs={'class': "form-control"}),
            'comment': forms.Textarea(attrs={'cols': 100, 'rows': 20, 'class': "form-control"}),
        }


class CreateAuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('b_day', 'photo', 'about')
        exclude = ('slug','name', 'last_name',  'author_user',  'email','active', 'number_of_news','age','number_days_of_activity')
        labels = {
            'b_day': gl('День рождения'),
            'photo': gl('Фото'),
            'about': gl('О вас'),
        }
        widgets = {
            'about': forms.Textarea(attrs={'cols': 50, 'rows': 10 }),
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


# class AddNewsForm(forms.ModelForm):
#     class Meta:
#         model = News
#         fields = '__all__'

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
