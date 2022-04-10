from django.db import models

# Create your models here.
from users.models import User
from orders.models import OrderAddress
 
class Transactions(models.Model):
    transaction = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderAddress, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, null= True)

    def __str__(self):
        return str(self.transaction)

