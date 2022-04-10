from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.forms import ModelForm
from user.models import User ,OTP_Data
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib import auth
from books.models import Books

class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )


class OTPForm(ModelForm):
    
    class Meta:
        model = OTP_Data
        
        fields=['phone_number','otp']        


class UserForm(ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields=['phone_number','email','password','confirm_password'] 
    
        widgets = {
        'password': forms.PasswordInput(),
        'confirm_password': forms.PasswordInput(),

        'phone_number': PhoneNumberPrefixWidget,
    }  

       
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get("confirm_password")

        if not phone_number and not email and not password:
            raise forms.ValidationError('You have to write something!')
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
    

    def clean_phone_number(self):
        try:
            users = User.objects.get(phone_number__iexact=str(self.cleaned_data['phone_number']))
        except User.DoesNotExist:
            return self.cleaned_data['phone_number']
        raise forms.ValidationError(_("The phone number already exists. Please try another one."))

    def clean_email(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("The Email already exists. Please try another one."))
    
    def save(self):
        password = self.cleaned_data.pop('password')
        u = super().save()
        u.set_password(password)
        u.save()
        return u



class SignupFrom(ModelForm):
    
    class Meta:
        model = User
        #password = forms.CharField(widget=forms.PasswordInput())
        fields=['phone_number'] 
        widgets = {
        
        'phone_number': PhoneNumberPrefixWidget,
    }  

       
    def clean(self):

        cleaned_data = super( SignupFrom, self).clean()
        phone_number = cleaned_data.get('phone_number')
       

        if not phone_number:
            raise forms.ValidationError('You have to write something!')


class LoginForm(forms.Form):
    phone_number = forms.CharField(widget=PhoneNumberPrefixWidget, label=_(u'Your phone_number'))
    password = forms.CharField(widget=forms.PasswordInput, label=_(u'Password'))

    def clean_phone_number(self):

        data = self.cleaned_data['phone_number']
        if not data:
            raise forms.ValidationError(_("Please enter phone_number"))
        return data

    def clean_password(self):

        data = self.cleaned_data['password']
        if not data:
            raise forms.ValidationError(_("Please enter your password"))
        return data

    def clean(self):
        # import pdb;pdb.set_trace()

        try:
            phone_number = self.cleaned_data['phone_number']
        except User.DoesNotExist:
            raise forms.ValidationError(_("No such phone_number registered"))
        password = self.cleaned_data['password']

        self.user = auth.authenticate(phone_number=phone_number, password=password)
        if self.user is None or not self.user.is_active:
            raise forms.ValidationError(_("phone_number or password is incorrect"))
        return self.cleaned_data


class SearchForm(ModelForm):
    
    class Meta:
        model = Books
        #password = forms.CharField(widget=forms.PasswordInput())
        fields=['book_name', 'category_id'] 


    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        name = cleaned_data.get('name')
        category = cleaned_data.get('category')
       