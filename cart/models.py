from django.db import models

from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from users.models import User

class CartData(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
   book_info = JSONField()
   status = models.IntegerField(choices=((1, _("paid")),
                                       (2, _("unpaid"))),
                                       default=2)
   def __str__(self):
   	return str(self.user)
