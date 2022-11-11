from email import message
from django import forms
from django.forms import formset_factory
from .models import Invoice


class InvoiceForm(forms.Form):
    customer = forms.CharField(
        label='Customer',
        widget= forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Customer Name',
            'rows':1
        })
    )
    customer_email = forms.CharField(
        label='Customer Email',
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': 'customer@emailid.com',
            'rows':1
        })
    )

    billing_address = forms.CharField(
         label='Billing Address',
         widget=forms.TextInput(attrs={
             'class': 'form-control',
             'placeholder':'',
             'rows':1
         })
    )

    message = forms.CharField(
        label='Message/Note',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'message',
            'rows':1
        })
    )

class LineItemForm(forms.Form):
    
    service = forms.CharField(
        label='Service/Product',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Service Name'
        })
    )
    description = forms.CharField(
        label='Description',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Product description',
            "rows":1
        })
    )
    quantity = forms.IntegerField(
        label='Qty',
        widget=forms.TextInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity'
        }) #quantity should not be less than one
    )
    rate = forms.DecimalField(
        label='Rate $',
        widget=forms.TextInput(attrs={
            'class': 'form-control input rate',
            'placeholder': 'Rate'
        })
    )
   
    
LineItemFormset = formset_factory(LineItemForm, extra=1)