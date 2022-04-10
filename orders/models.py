from django.db import models
from books.models import Books
from users.models import User, Timestamp
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class OrderAddress(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_info = JSONField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    status      = models.CharField(max_length=20, default='pending')
    # price       = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    id          = models.OneToOneField(Books, related_name='order_items', on_delete=models.CASCADE, primary_key=True)
    order_id    = models.ForeignKey(OrderAddress, related_name='items', on_delete=models.CASCADE)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    status      = models.CharField(max_length=10)
    quantity    = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

class OrderDetail(Timestamp):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   order_info = JSONField()