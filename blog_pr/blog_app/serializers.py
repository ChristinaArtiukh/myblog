from rest_framework import serializers
from .models import Book, Writer, Publisher, Genre


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('__all__')

