from django.db import models
import jsonfield
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
import datetime
from users.models import User
# from orders.models import OrderAddress

class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
 

class BookCategory(Timestamp):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.genre
   

    def get_absolutes_url(self):
        return reverse('users:product_list_by_category', args=[self.id])



class Author(Timestamp):
    id      = models.AutoField(primary_key=True)
    name    = models.CharField(max_length=50, db_index=True)
    email   = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

YEAR_CHOICES = []
for r in range(1984, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

RENT = 'R'
BUY = 'B'
BOOK_CONDITION_CHOICES = (
    (RENT, 'rent'),
    (BUY, 'new'),
)

class Books(Timestamp):
    isbn_code   = models.CharField(primary_key=True, max_length=50, db_index=True)
    book_name   = models.CharField(max_length=50, db_index=True)
    # image       = models.ImageField(upload_to='books/%Y/%m/%d', blank=True)
    image       = models.TextField(blank=True, null=True) 
    language    = models.CharField(max_length=50,blank=True, db_index=True)
    mrp         = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)   
    book_description = models.TextField(blank=True, null=True)
    binding_type= models.CharField(max_length=50, db_index=True)
    category_id = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name='books')
    author_id   = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    #stock
    buy_count = models.PositiveIntegerField()
    rent_count = models.PositiveIntegerField()
    book_condition =models.CharField(max_length=10, choices=BOOK_CONDITION_CHOICES, default=BUY)                                    
    publication_year =  models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)


    def __str__(self):
        return self.book_name

    def get_absolute_url(self):
        return reverse('books:books_detail', args=[self.isbn_code])



#pushtakkosh scrapping data saved
class BooksDetail(Timestamp):
    name        = models.TextField()
    mrp         = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    description = models.TextField(blank=True, null=True)
    image       = models.TextField(blank=True, null=True)



    def __str__(self):
        return self.name



# indiabookstore scrapping data saved 
class BooksModel(Timestamp):
    Name = models.TextField()
    ISBN_13 = models.CharField(max_length=50, db_index=True)
    Author  = models.CharField(max_length=50, db_index=True)
    Publisher = models.CharField(max_length=50, db_index=True)
    Rating = models.CharField(max_length=50, blank=True, null=True)
    ISBN_10 = models.CharField(max_length=50, db_index=True)
    Number_of_pages = models.IntegerField(blank=True, null=True)
    Language = models.CharField(max_length=50, blank=True, null=True)
    Edition = models.CharField(max_length=50, blank=True, null=True)
    Dimensions = models.CharField(max_length=50, blank=True, null=True)
    Book_Description = models.TextField(blank=True, null=True)
    Image_URL = models.TextField(blank=True, null=True)
    Prices  = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.Name 

class Rental(Timestamp):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    borrow = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now=True)
    #order date
    # order_date = models.ForeignKey(OrderAddress, on_delete=models.CASCADE)
    return_date = models.DateTimeField(auto_now=True)
    actual_return_date = models.DateTimeField(auto_now=True)
    return_condition = models.CharField(max_length=50, blank=True, null=True)
    rate_per_day = models.DecimalField(default=0.0 ,max_digits=3, decimal_places=1,)
   
    def __str__(self):
        return str(self.book)        


