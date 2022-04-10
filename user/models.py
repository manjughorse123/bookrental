# from django.db import models
# import jsonfield
# from django.urls import reverse
# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser, User,PermissionsMixin
# )
# from django.utils.translation import ugettext_lazy as _
# from phonenumber_field.modelfields import PhoneNumberField
# from datetime import datetime

# class Timestamp(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract=True

# class OTP_Data(Timestamp):
#     otp = models.IntegerField(blank=True,null=True)    
#     phone_number = models.CharField(max_length=13, blank=True,null=True)

# class UserManager(BaseUserManager):
#     def create_user(self, phone_number, email=None, password=None):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not phone_number:
#             raise ValueError('Users must have an phone_number ')
#         # phone_number=self.phone_number
#         user = self.model(
#             phone_number=phone_number, 
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         user.is_staff = True
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

#     def create_staffuser(self, phone_number, password):
#         """
#         Creates and saves a staff user with the given phone_number and password.
#         """
#         user = self.create_user(
#             phone_number, email=email,
#             password=password,
#         )
#         user.is_active = True
#         user.is_staff = True
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, phone_number, email, password):
#         # import pdb; pdb.set_trace()

#         """
#         Creates and saves a superuser with the given phone_number and password.
#         """
#         user = self.create_user(
#             phone_number,email=email,
#             password=password,
#         )
#         user.email=email
#         user.is_staff = True
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser, PermissionsMixin, Timestamp):
#     phone_number = PhoneNumberField(unique=True)
#     name = models.CharField(max_length=80, blank=True)
#     email = models.EmailField(_('email address'), blank=True, null=True)
#     first_name = models.CharField(_('first name'), max_length=30, blank=True)
#     last_name = models.CharField(_('last name'), max_length=30, blank=True)
#     user_type = models.IntegerField(choices=((1, _("admin")),
#                                         (2, _("user")),
#                                         (3, _("supplier"))),
#                                         default=2,)
#     is_action = models.BooleanField(default=False)
#     is_phone_number_verified = models.BooleanField(default=False)
#     is_email_verified = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False) 
    

#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = ['email']     

#     objects = UserManager()

#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')

#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.email

#     def __str__(self):
#         return self.email if  self.email else str(self.phone_number)    

#     def get_short_name(self):
#         '''
#         Returns the short name for the user.
#         '''
#         return self.email
 
#     def is_staff(self):
#         "Is the user a member of staff?"
#         return self.is_staff

   
#     def is_admin(self):
#         "Is the user a admin member?"
#         return self.is_admin

    
#     def is_active(self):
#         "Is the user active?"
#         return self.is_active

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     def user_post_save(sender, instance, signal, *args, **kwargs):
#         #import pdb; pdb.set_trace()
#         if not instance.is_verified:
#             # Send verification email
#             send_verification_email.delay(instance.pk)
     
#         signals.post_save.connect(user_post_save, sender=User)

#     def save(self, *args, **kwargs):
#         # import pdb; pdb.set_trace()
#         if not self.pk:
#             # if we dont have a pk set yet, it is the first time we are saving. Nothing to duplicate.
#             super(User, self).save(*args, **kwargs)
#             # Create Profile and supplier acooding to user_role
#             wallet = Wallet()
#             wallet.save()
#             if self.user_type == "user":
#                 profile = Profile(user_id= self, wallet_id=wallet)
#                 profile.save()
#             elif self.user_type == "supplier":
#                 from supplier.models import Supplier
#                 supplier = Supplier(user= self, wallet=wallet)
#                 supplier.save()
#         else:
#             super(User, self).save(*args, **kwargs)

#     def __str__(self):
#         return 'MyUser {}'.format(self.id)





# class Wallet(Timestamp):
#     id      = models.AutoField(primary_key=True)
#     balance = models.IntegerField(default=0)
#     reward  = models.IntegerField(default=0)

#     def __str__(self):
#         return str(self.id)

# class Location(Timestamp):
#     id      = models.AutoField(primary_key=True)
#     location= jsonfield.JSONField(blank=True)
#     address = models.TextField(blank=True)
#     city    = models.TextField(blank=True)
#     reward  = models.IntegerField(blank=False)
#     name    = models.CharField(max_length=100, blank=True)
#     phone   = PhoneNumberField(blank=True)

# class Profile(Timestamp):
#     user_id     = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     wallet_id   = models.OneToOneField(Wallet, on_delete=models.CASCADE)
#     default_location = models.OneToOneField(Location, on_delete=models.CASCADE, blank=False, null=True)
#     user_role   = models.CharField(max_length=100, db_index=True)
#     address1    = models.CharField(max_length=100, blank=False, null=True)
#     address2    = models.CharField(max_length=100, blank=True, null=True)
#     city        = models.CharField(max_length=30, blank=True, null=True)
#     postal_code = models.IntegerField(blank=True, null=True)
#     phone_number= models.IntegerField(null=True, blank=False)
#     profile_pic = models.ImageField(null=True, blank=True)
#     education   = models.CharField(max_length=20, blank=True)
#     field       = models.CharField(max_length=50, blank=True)
#     favourite_book = models.CharField(max_length=30, blank=True)


# class LoginHistory(Timestamp):
#     ip_address = models.GenericIPAddressField()