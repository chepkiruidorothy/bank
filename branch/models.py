from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class Loan(models.Model):
    name = models.CharField(max_length=30, default="name")
    description = models.CharField(max_length=100)
    amount= models.DecimalField( max_digits=12, decimal_places=2)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    duration=models.IntegerField()
    pending=models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Account(models.Model):
    name=models.CharField(max_length=30,default="")
    balance=models.DecimalField( max_digits=12, decimal_places=2)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Transaction(models.Model):
        CHOICES=(
            ('WD', 'Withdrawal'),
            ( 'DP','Deposit'),
            )
        amount=models.DecimalField(max_digits=12, decimal_places=2)
        type=models.CharField(max_length=30, choices = CHOICES)
        to_account = models.ForeignKey(Account,on_delete=models.CASCADE, related_name='to_account')
        account=models.ForeignKey(Account,on_delete=models.CASCADE,  related_name='account')
        timestamp = models.DateTimeField(auto_now_add = True)

        def __str__(self):
            return self.type
