from django import forms

class AddToCartForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, initial=1)
