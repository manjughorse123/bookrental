from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.forms import ModelForm
from users.models import User ,OTP_Data, Choices_User
from phonenumber_field.widgets import PhoneNumberPrefixWidget
# from django.contrib.auth import authenticate
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
    # import pdb;pdb.set_trace()
    phone_number = forms.CharField()
    countries = forms.CharField()
    user_type = forms.ChoiceField(choices=Choices_User)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields=['phone_number','name','email','password','confirm_password', 'user_type'] 
    
        widgets = {
        'password': forms.PasswordInput(),
        'confirm_password': forms.PasswordInput(),
        
    }  

       
    # def clean(self):
    #     import pdb;pdb.set_trace()
    #     cleaned_data = super(UserForm, self).clean()
    #     phone_number = cleaned_data.get('phone_number')+
    #     email = cleaned_data.get('email')
    #     countries = cleaned_data.get('countries')
    #     name = cleaned_data.get('name')
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get("confirm_password")

    def clean(self):
        
        cleaned_data = super(UserForm, self).clean()
        number = self.cleaned_data['phone_number']
        email = self.cleaned_data.get("email")
        countries = self.cleaned_data['countries']
        user_type = self.cleaned_data['user_type']
        name = self.cleaned_data['name']
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        phone_number = self.cleaned_data['phone_number']=countries+number
 

        if not phone_number and not email and not password:
            raise forms.ValidationError('You have to write something!')
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
    

    def clean_phone_number(self):
        try:
            user = User.objects.get(phone_number__iexact=str(self.cleaned_data['phone_number']))
        except User.DoesNotExist:
            return self.cleaned_data['phone_number']
        raise forms.ValidationError(_("The phone number already exists. Please try another one."))

    def clean_email(self):
        
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("The Email already exists. Please try another one."))
    
    # def save(self):
    #     password = self.cleaned_data.pop('password')
    #     u = super().save()
    #     u.set_password(u.password)
    #     u.save()
    #     return u

class LoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    countries = forms.CharField()
    phone_number = forms.CharField()
    class Meta:
        model = User
        fields=['phone_number','password'] 
    
        widgets = {
        'password': forms.PasswordInput(),
       
    }  

    def clean_phone_number(self):
        
        data = self.cleaned_data['phone_number']
        if not data:
            raise forms.ValidationError(_("Please enter phone_number"))
        return data
    def clean_countries(self):
        
        data = self.cleaned_data['countries']
        if not data:
            raise forms.ValidationError(_("Please enter phone_number"))
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if not data:
            raise forms.ValidationError(_("Please enter your password"))
        return data

    def clean(self):
       
        number = self.cleaned_data['phone_number']
        countries = self.cleaned_data['countries']
        phone_number = self.cleaned_data['phone_number']=countries+number
 
        try:
            phone_number = self.cleaned_data['phone_number']
        except User.DoesNotExist:
            raise forms.ValidationError(_("No such phone_number registered"))
        password = self.cleaned_data['password']

        self.user = auth.authenticate(phone_number=phone_number, password=password)
        if self.user is None or not self.user.is_active:
            raise forms.ValidationError(_("phone_number or password is incorrect"))
        return self.cleaned_data

# class LoginForm(forms.Form):
#     phone_number = forms.CharField(label=_(u'Your phone_number'))
#     countries = forms.CharField(label=_(u'Your country code'))
#     # phone_number = forms.CharField(widget=PhoneNumberPrefixWidget, label=_(u'Your phone_number'))
#     password = forms.CharField(widget=forms.PasswordInput, label=_(u'Password'))

#     def clean_phone_number(self):
        
#         data = self.cleaned_data['phone_number']
#         if not data:
#             raise forms.ValidationError(_("Please enter phone_number"))
#         return data
#     def clean_countries(self):
        
#         data = self.cleaned_data['countries']
#         if not data:
#             raise forms.ValidationError(_("Please enter phone_number"))
#         return data

#     def clean_password(self):
#         data = self.cleaned_data['password']
#         if not data:
#             raise forms.ValidationError(_("Please enter your password"))
#         return data

#     def clean(self):
#         import pdb;pdb.set_trace()
#         try:
#             phone_number =self.cleaned_data['countries']+self.cleaned_data['phone_number']
#         except User.DoesNotExist:
#             raise forms.ValidationError(_("No such phone_number registered"))
#         password = self.cleaned_data['password']

#         self.user = auth.authenticate(phone_number=phone_number, password=password)
#         if self.user is None or not self.user.is_active:
#             raise forms.ValidationError(_("phone_number or password is incorrect"))
#         return self.cleaned_data