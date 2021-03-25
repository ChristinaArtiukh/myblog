from django_filters import rest_framework as filters, fields
from django_filters.filterset import BaseFilterSet

from .models import Book, Writer, Publisher, Genre
from django_filters.widgets import CSVWidget, BaseCSVWidget
from django import forms
from django.db import models


ORDER_CHOICES = [
        ["name", "по алфавиту"],
        ["price", "дешевые сверху"],
        ["-price", "дорогие сверху"]
    ]


class BookFilter(filters.FilterSet):

    publisher = filters.CharFilter(field_name='publisher__publisher_name', lookup_expr='iexact')
    writer = filters.CharFilter(field_name='writer__writer_name', lookup_expr='iexact')
    genre = filters.CharFilter(field_name='genre__genre_name', lookup_expr='iexact')

    ordering = filters.ChoiceFilter(choices=ORDER_CHOICES)

    class Meta:
        model = Book
        exclude = ['photo1', 'photo2']
        fields = ['writer', 'publisher', 'genre', 'title']

    # def get_queryset(self):
    #     publisher = Publisher.objects.all()
    #     if publisher != '' and publisher is not None:
    #         queryset = self.queryset.filter(publisher=self.kwargs.get('publisher__publisher_name'))
    #         return queryset


#


#
#
# class BookFilter(filters.FilterSet):
#     genre = filters.ModelMultipleChoiceFilter(queryset=Genre.objects.all(), widget = forms.CheckboxSelectMultiple)
#     genres = CustomFilterList(field_name='genre__genre_name')
#
#     class Meta:
#         model = Book
#         fields = ['genres', 'genre']


