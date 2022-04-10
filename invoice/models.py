from django.db import models
from books.models import Books
from users.models import User, Timestamp
from orders.models import OrderAddress

class Invoice(Timestamp):

    id = models.AutoField(primary_key=True)
    order_id= models.ForeignKey(OrderAddress, on_delete=models.CASCADE)
    # order_id= models.IntegerField(default=0)
    
    invoice_num = models.IntegerField(default=0)
    invoice_date = models.DateTimeField(auto_now=True)
    order_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'Invoice')
    payment_type = models.CharField(max_length=255)
    invoice_type = models.CharField(max_length=255)
    order_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    delaivery_charge = models.CharField(max_length=255)
    delaivery_adress = models.CharField(max_length=255)
    invoice_status = models.TextField()
    discount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    tax = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    # total_FLOAT = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sub_total = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    cencle_reason = models.CharField(max_length=255)
    insturction = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'invoice'

    # def __str__(self):
    #     return self.user

class InvoiceItem(Timestamp):

    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name = 'InvoiceItem')
    item = models.ForeignKey(Books, on_delete=models.CASCADE, related_name = 'InvoiceItem') 
    quantity = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    discount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    class Meta:
        db_table = 'invoice_item'


