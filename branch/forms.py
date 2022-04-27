from django import forms
from django.forms import ModelForm
from .models import Account, Loan, Customer

class AccountForm(forms.ModelForm):
    name=forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    balance= forms.DecimalField( label='Balance ', widget = forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=Account
        fields=['name','balance', 'customer']

class LoanForm(forms.ModelForm):
    amount= forms.DecimalField( label='Amount ', widget = forms.TextInput(attrs={'class':'form-control'}))
    duration=forms.IntegerField(label='Duration', widget = forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model= Loan
        fields=['amount','duration','customer']

class CustomerForm(forms.ModelForm):
        class Meta:
            model=Customer
            fields=['user']


class TransactForm(forms.Form):

    amount= forms.DecimalField( label='Amount ', widget = forms.TextInput(attrs={'class':'form-control'}))

class TransForm(forms.Form):

    amount= forms.DecimalField( label='Amount ', widget = forms.TextInput(attrs={'class':'form-control'}))
    duration=forms.IntegerField(label='Duration', widget = forms.TextInput(attrs={'class':'form-control'}))
