from django import forms
from django.forms import ModelForm
from .models import Account, Loan, Customer


class TransactForm(forms.Form):

    amount= forms.DecimalField( label='Amount ', widget = forms.TextInput(attrs={'class':'form-control'}))

class LoanForm(forms.Form):

    amount= forms.DecimalField( label='Amount ', widget = forms.TextInput(attrs={'class':'form-control'}))
    duration=forms.IntegerField(label='Duration', widget = forms.TextInput(attrs={'class':'form-control'}))

class TransferForm(forms.Form):

    amount= forms.DecimalField( label='Amount ', widget = forms.TextInput(attrs={'class':'form-control'}))
    acc_name  =forms.CharField( label='Account name', widget = forms.TextInput(attrs={'class':'form-control'}))
