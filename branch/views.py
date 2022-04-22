from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Customer,Loan, Account,Transaction
from django.views.generic import UpdateView, ListView
from .forms import AccountForm, LoanForm, CustomerForm, TransactForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
import random
import string
from decimal import Decimal

@login_required
def home(request):
    accounts = Account.objects.filter(customer__user = request.user)
    loans = Loan.objects.filter(name=request.user)
    return render(request, 'home.html',
        {"accounts":accounts, "loans":loans}
    )

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create(request):
    customer = Customer.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        Account.objects.create(
        name = random_string_generator(),
        customer = customer,
        balance = 0
        )
        return HttpResponse('Account created successfully')

    else:
        pass
    return render(request,'create.html')

def request_loan(request,pk):
    account = get_object_or_404(Account, pk=pk)
    loans = Loan.objects.filter(customer__user=request.user)
    customer = Customer.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            amount = request.POST.get('amount')
            duration = request.POST.get('duration')
            amo = Decimal(amount)
            print(amo)
            form.save()
            Loan.objects.create(
            amount=amo,
            duration=duration,
            customer=customer,
            pending=True
            )
            return render(request,'loan_requested.html', {'form':form, "loans":loans,"account":account})
    if request.method == 'GET':
        form=LoanForm()
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
