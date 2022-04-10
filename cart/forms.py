from django import forms


CHOICES = [(i, str(i)) for i in range(1, 21)]



class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=CHOICES,
                                      coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

DAIYS = [(i, str(i)) for i in range(1, 50)]

class CartRentForm(forms.Form):

    days_for_rent = forms.TypedChoiceField(choices=DAIYS,
    								coerce=int)