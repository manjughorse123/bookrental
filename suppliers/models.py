from django.db import models

# Create your models here.
from datetime import datetime
from users.models import User, Wallet
# from books.models import BOOK_CONDITION_CHOICES


BOOK_CONDITION_CHOICES = (

    ( 'rent' ,'RENT'),
    ( 'new' ,'BUY'),
)


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Suppliers(Timestamp):
    user     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='suppliers')
    wallet   = models.OneToOneField(Wallet, on_delete=models.CASCADE, related_name='suppliers')
    address1    = models.CharField(max_length=50, blank=False, null=False)
    address2    = models.CharField(max_length=50,blank=True, null=True)
    city        = models.CharField(max_length=50,blank=True, db_index=True)
    postal_code = models.IntegerField(blank=False, null=True)
    profile_pic = models.ImageField(height_field=None, width_field=None, max_length=100)

    class Meta:
        db_table='suppliers'
    
    def __str__(self):
        return self.user.name

class Shop(Timestamp):
    owner_id    = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='shop')
    name        = models.CharField(max_length=50, blank=False, null=False)
    address     = models.CharField(max_length=50, blank=False, null=False)
    city        = models.CharField(max_length=50,blank=True, db_index=True)
    phone_number = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.name
    class Meta:
        db_table='shop'

class SupplierBooks(Timestamp):

    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='SupplierBooks')
    isbn_code   = models.CharField(primary_key=True, max_length=50, db_index=True)
    book_name   = models.CharField(max_length=50, db_index=True)
    image       = models.TextField(blank=True, null=True) 
    language    = models.CharField(max_length=50,blank=True, db_index=True)
    mrp         = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)   
    book_description = models.TextField(blank=True, null=True)
    binding_type = models.CharField(max_length=50, db_index=True)
    category = models.CharField(max_length=50, db_index=True)
    author   = models.CharField(max_length=50, db_index=True)
    #stock
    buy_count = models.PositiveIntegerField()
    rent_count = models.PositiveIntegerField()
    book_condition = models.CharField(max_length=10, choices=BOOK_CONDITION_CHOICES, default='new')                                    
    publication_year =  models.IntegerField(default=1990)


    class Meta:
        db_table='supplierbooks'
        
    def __str__(self):
        return self.book_name

    def get_absolute_url(self):
        return reverse('supplierbooks:updated', args=[self.isbn_code])