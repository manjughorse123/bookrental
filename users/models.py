# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import signals
from users.tasks import *



# Create your models here.
class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

    class Meta:
        abstract=True


class OTP_Data(Timestamp):
    otp = models.IntegerField(blank=True, null=True)    
    phone_number = PhoneNumberField()

# mobile = PhoneNumberField(required=True, country='+91')
class UserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone_number ')
        # phone_number=self.phone_number
        user = self.model(
            phone_number=phone_number, 
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone_number, password):
        """
        Creates and saves a staff user with the given phone_number and password.
        """
        user = self.create_user(
            phone_number, email=email,
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password):
        # import pdb; pdb.set_trace()

        """
        Creates and saves a superuser with the given phone_number and password.
        """
        user = self.create_user(
            phone_number,email=email,
            password=password,
        )
        user.email=email
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user
Choices_User=(('admin','Admin'),
                ('user','User'),
        ('supplier','Supplier'),)

class User(AbstractBaseUser, PermissionsMixin, Timestamp):
    
    phone_number = PhoneNumberField(unique=True ,)
    name = models.CharField(max_length=80, blank=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=30, blank=True)
    user_type = models.CharField(max_length=30, choices=Choices_User,
                                        default='user')
    is_action = models.BooleanField(default=False)
    is_phone_number_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False) 
     
    
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_staff

   
    def is_admin(self):
        "Is the user a admin member?"
        return self.is_admin

    
    def is_active(self):
        "Is the user active?"
        return self.is_active

    def __str__(self):              # __unicode__ on Python 2
        return self.email if  self.email else str(self.phone_number)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

 
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     return self.staff

   
    # def is_admin(self):
    #     "Is the user a admin member?"
    #     return self.admin

    
    # def is_active(self):
    #     "Is the user active?"
    #     return self.active


    def user_post_save(sender, instance, signal, *args, **kwargs):
        #import pdb; pdb.set_trace()
        if not instance.is_verified:
            # Send verification email
            send_verification_email(instance.pk)
     
        signals.post_save.connect(user_post_save, sender=User)
    #instance.post.save()


class Wallet(Timestamp):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='wallet')
    balance = models.IntegerField(default=0)     
    
    reward = models.IntegerField(default=0)            

    def __str__(self):
        return str(self.id)
    
    class meta:
        db_table = 'wallet'

class walletHistory(models.Model): 
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='wallet_history')
    #action = models.TextField() 
    desc = models.TextField(null=True, blank=True)
    amount = models.DecimalField(default=0.0, max_digits=3,decimal_places=3)
    #type = 
        
    def __str__(self):
        return str(self.user)

# class UserLocation(Timestamp):
#     user =  models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )           
#     user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='location')
#     location =models.TextField()         
#     address = models.TextField()            
#     city = models.CharField(max_length=30)          
#     is_active = models.BooleanField(default=True)          
   
#     def __str__(self):
#         return self.user  

#     class Meta:
#         db_table = 'Userlocation'


class UserProfile(Timestamp):  
    user =  models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)
    #current_location = models.ForeignKey(UserLocation, on_delete=models.CASCADE)
    current_location = models.CharField(max_length=20, blank=True) 
    postal_code = models.IntegerField(default=0) 
    profile = models.URLField("Website", blank=True) 
    foodie_level = models.IntegerField(default=0)
    no_of_recommendations = models.IntegerField(default=0) 
    no_of_review = models.IntegerField(default=0)          
   
    def __str__(self):
        return self.user.name 

    class Meta:
        db_table = 'user_profile'


class UserImageHistory(Timestamp):
    user =  models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='image_history')
    profile = models.URLField("Website", blank=True) 

    def __str__(self):
        return (self.user.name + self.profile) 

    class Meta:
        db_table = 'user_image_history'



class LoginHistory(Timestamp):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='login_history')
    
    ip = models.GenericIPAddressField()  

    def __str__(self):
        return self.user.name 

    class Meta:
        db_table = 'login_history'


class UserRecommendation(Timestamp):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='recommended')
    recommend_type = models.IntegerField(choices=((1, _("dish")),
                                                (2, _("restaurents "))),
                                        default=1)
 
    recommend_id = models.IntegerField(default=0)


    class Meta:
        db_table = 'user_recommendation'

