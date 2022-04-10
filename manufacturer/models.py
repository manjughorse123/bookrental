from django.db import models
from users.models import Timestamp
from phonenumber_field.modelfields import PhoneNumberField


class Manufacturer(Timestamp):
    id = models.AutoField(primary_key=True)
    owner_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    email = models.EmailField( verbose_name='email address',
        max_length=255)
    postal_code = models.IntegerField(default=0)
    company_type = models.CharField(max_length=255)
    #city = models.TextField()
    address = models.TextField()

    class Meta:
        db_table = 'manufacturer'
    