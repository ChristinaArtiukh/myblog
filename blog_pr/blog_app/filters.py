
from django_filters import rest_framework as filters
from requests import models

from .models import Book, Writer, Publisher, Genre


# class BookFilterBar(filters.FilterSet):
#     ordering = filters.CharFilter(field_name='ordering')
#
#     class Meta:
#         model = Book
#         exclude = ['photo1', 'photo2']
#         fields = ['ordering', ]


class BookFilterSidebar(filters.FilterSet):

    publisher = filters.CharFilter(field_name='publisher__publisher_name')
    writer = filters.CharFilter(field_name='writer__writer_name')
    genre = filters.CharFilter(field_name='genre__genre_name')

    class Meta:
        model = Book
        exclude = ['photo1', 'photo2']
        fields = {
            'writer': ['exact'],
            'publisher': ['exact'],
            'genre': ['exact']
                  }


