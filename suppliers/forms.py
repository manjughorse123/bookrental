from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.forms import ModelForm
from users.models import User ,OTP_Data, Choices_User
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from django.contrib import auth
from suppliers.models import SupplierBooks, BOOK_CONDITION_CHOICES
from books.models import Books , Author


class BookForm(ModelForm):
 
    class Meta:
        model = SupplierBooks
        fields= '__all__'
    

    def clean(self):
        
        cleaned_data = super(BookForm, self).clean()
        supplier = self.cleaned_data['supplier']
        isbn_code = self.cleaned_data['isbn_code']
        book_name = self.cleaned_data['book_name']
        binding_type = self.cleaned_data['binding_type']
        image = self.cleaned_data['image']
        mrp = self.cleaned_data['mrp']
        language = self.cleaned_data['language']
        book_description = self.cleaned_data['book_description']
        category = self.cleaned_data['category']
        author = self.cleaned_data['author']
        buy_count = self.cleaned_data['buy_count']
        rent_count = self.cleaned_data['rent_count']
        book_condition = self.cleaned_data.get('book_condition')
        publication_year = self.cleaned_data['publication_year']

        if not isbn_code and not book_name and not author:
            raise forms.ValidationError('You have to write something!')
        return self.cleaned_data
       
    

    # def clean_author(self):
    #     import pdb;pdb.set_trace()
    #     try:
    #         author = Author.objects.get(name_exact=self.cleaned_data['author'])
    #     except User.DoesNotExist:
    #         return self.cleaned_data['author']
    #     raise forms.ValidationError(_("The phone number already exists. Please try another one."))

    # def clean_email(self):
        
    #     try:
    #         user = User.objects.get(email__iexact=self.cleaned_data['email'])
    #     except User.DoesNotExist:
    #         return self.cleaned_data['email']
    #     raise forms.ValidationError(_("The Email already exists. Please try another one."))
