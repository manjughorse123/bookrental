from rest_framework import serializers
from books.models import Books

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('pk', 'book_name', 'language', 'book_description','category_id','author_id')
        # fields = '__all__'