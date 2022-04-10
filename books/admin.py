from django.contrib import admin

# Register your models here.
from books.models import Books,BookCategory,Author,BooksDetail, BooksModel, Rental 

admin.site.register(Books)
admin.site.register(BookCategory)
admin.site.register(Author)
admin.site.register(BooksModel)
admin.site.register(BooksDetail)
admin.site.register(Rental)
