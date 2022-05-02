from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Customer,Loan, Account,Transaction
from django.contrib.auth.models import User
from django.views.generic import UpdateView, ListView
from .forms import  TransactForm, LoanForm, TransferForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
import random
import string
from decimal import Decimal

@login_required
def home(request):
    accounts = Account.objects.filter(customer__user = request.user)
    loans = Loan.objects.filter(name=request.user)
    return render(request, 'home.html',{"accounts":accounts, "loans":loans})

def index(request):
    return render(request, 'index.html')

def randomGen():
    # return a 6 digit random number
    return (random.uniform(100000, 999999))

def random_string_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create(request):
    accounts = Account.objects.filter(customer__user=request.user)
    user = get_object_or_404(User,username__iexact=request.user)
    if request.method == 'POST':

        customer, created = Customer.objects.get_or_create(user=request.user)
        print(customer)
        Account.objects.create(
            name = random_string_generator(),
            customer = customer,
            balance = 0
        )
        return render(request, 'created.html',{'accounts':accounts})

        customer = Customer.objects.filter(user=request.user)[0]
    else:
        pass
    return render(request,'create.html')


def request_loan(request,pk):
    form=LoanForm()
    account = get_object_or_404(Account, pk=pk)
    loans = Loan.objects.filter(customer__user=request.user)
    user = get_object_or_404(User,username__iexact=request.user)
    customer = Customer.objects.filter(user=request.user)[0]
    if request.method == 'GET':
        return render(request,'request_loan.html', {'form':form, "loans":loans,"account":account})
    if request.method == 'POST':
        form=LoanForm(request.POST)
        if form.is_valid():
            amount = request.POST.get('amount')
            duration = request.POST.get('duration')

            Loan.objects.create(
            amount=amount,
            duration=duration,
            customer=customer,
            pending=True
            )

            return render(request,'loan_requested.html', {'form':form, "loans":loans,"amount":amount, "account":account})
    else:
        return render(request,'request_loan.html', {'form':form, "loans":loans,"account":account})


def withdraw(request,pk):
    form=TransactForm()
    account = get_object_or_404(Account, pk=pk)
    balance = account.balance
    customer = Customer.objects.filter(user=request.user)[0]
    if request.method == "GET":
        return render(request,'withdraw.html', {'form':form, "account":account})

    if request.method == "POST":

        amount = request.POST.get('amount')
        amo = Decimal(amount)
        print(amo)
        print(balance)
        if form.is_valid:
            if (balance <= amo):
                return render(request, 'cannot_withdraw.html')
            else:
                transaction = Transaction.objects.create(
                amount=amo,
                type='Withdrawal',
                to_account = account,
                account= account
                )
                transaction.save()
                balance -= amo
                account.balance = balance
                account.save()
                return render(request, 'withdrawn.html',{'balance':balance, "account":account})

    else:
        return render(request,'withdraw.html', {'form':form, "account":account})


def deposit(request,pk):
    form=TransactForm()
    account = get_object_or_404(Account, pk=pk)
    balance = account.balance
    customer = Customer.objects.filter(user=request.user)[0]
    if request.method == "GET":
        return render(request,'deposit.html', {'form':form, "account":account})

    if request.method == "POST":
        amount = request.POST.get('amount')
        amo = Decimal(amount)
        print(amo)
        print(balance)
        if form.is_valid:
            transaction = Transaction.objects.create(
            amount=amo,
            type='Deposit',
            to_account = account,
            account= account
            )
            transaction.save()
            balance += amo
            account.balance = balance
            account.save()
            return render(request, 'deposited.html',{'balance':balance, "account":account})

    else:
        return render(request,'deposit.html', {'form':form, "account":account})

def statement(request,pk):
    account = get_object_or_404(Account, pk=pk)

    if request.method == 'GET':
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'statement.html', { 'account':account, 'transactions':transactions})

def loan_statement(request,pk):
    account = get_object_or_404(Account, pk=pk)
    loans = Loan.objects.filter(customer__user=request.user)
    if request.method == 'GET':
        return render(request, 'loan_statement.html', { 'account':account, 'loans':loans})

def send_money(request, pk):
    form=TransferForm()
    account = get_object_or_404(Account, pk=pk)
    balance = account.balance
    user = get_object_or_404(User,username__iexact=request.user)
    customer = Customer.objects.filter(user=request.user)[0]
    if request.method == "GET":
        return render(request,'transfer.html', {'form':form, "account":account})
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid:

            amount = request.POST.get('amount')
            acc_name = request.POST.get('acc_name')
            amo = Decimal(amount)
            try:
                to_account = Account.objects.get(name=acc_name)
            except Account.DoesNotExist:
                return render(request, 'account_not_found.html')
            to_account_balance = to_account.balance
            if (balance <= amo):
                return render(request, 'cannot_send.html')

            else:
                transfer = Transaction.objects.create(
                    amount=amo,
                    type='Transfer',
                    account= account,
                    to_account =to_account
                    )
                transfer.save()
                print(to_account)
                balance -= amo
                account.balance = balance
                to_account_balance += amo
                to_account.balance = to_account_balance
                account.save()
                to_account.save()

                return render(request, 'transferred.html',{'balance':balance, 'to_account_balance':to_account_balance,"to_account":to_account,"account":account})
    else:
        return render(request,'transfer.html', {'form':form, "account":account,"to_account":to_account})



def delete(request,pk):
    account = get_object_or_404(Account, pk=pk)
    balance = account.balance
    if request.method == 'GET':
        if balance != 0:
            return render(request, 'delete_error.html')
        else:
            return render(request,'delete.html')
    if request.method == 'POST':
        account.delete()
        return HttpResponseRedirect("/")
    return render(request,'delete.html')
