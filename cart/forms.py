from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BillingShippingInfo(forms.Form):
    name = forms.CharField(label='Name')
    email = forms.EmailField()
    address = forms.CharField(label='Address')
    city = forms.CharField(label='City')
    state = forms.CharField(label='State', max_length=30)
    zip_code = forms.CharField(label='Zip Code', max_length=6)

class PayemntInfo(forms.Form):
    payment_name = forms.CharField(label='Name')
    card_number = forms.CharField(max_length=20,label='Credit Card Number')
    month = forms.CharField(label='Month')
    year = forms.IntegerField(label='Year')
    cvc = forms.IntegerField(label='CVC')