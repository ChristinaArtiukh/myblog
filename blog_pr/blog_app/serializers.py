from rest_framework import serializers
from .models import Book, Writer, Publisher, Genre


class StringSerializer(serializers.StringRelatedField):
    def to_interval_value(self, value):
        return value


class BookSerializer(serializers.ModelSerializer):
    writer = StringSerializer(many=False)
    publisher = StringSerializer(many=False)
    genre = StringSerializer(many=True)

    class Meta:
        model = Book
        fields = ('__all__')

