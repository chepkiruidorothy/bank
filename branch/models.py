from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user=models.OneToOneField(User, unique=True, default='', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Loan(models.Model):
    name = models.CharField(max_length=30, default="name")
    description = models.CharField(max_length=100)
    amount= models.DecimalField( max_digits=12, decimal_places=2)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    duration=models.IntegerField()
    pending=models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=30, unique=True, default='')
    balance=models.DecimalField( max_digits=12, decimal_places=2)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
        CHOICES=(
            ('WD', 'Withdrawal'),
            ( 'DP','Deposit'),
            ( 'TF','Transfer'),
            )
        amount=models.DecimalField(max_digits=12, decimal_places=2)
        type=models.CharField(max_length=30, choices = CHOICES)
        to_account = models.ForeignKey(Account,on_delete=models.CASCADE, related_name='to_account')
        account=models.ForeignKey(Account,on_delete=models.CASCADE,  related_name='account')
        timestamp = models.DateTimeField(auto_now_add = True)

        def __str__(self):
            return self.type

class Singleton(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Singleton, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

class Setting(Singleton):
    customer = models.ForeignKey(Customer,null=False, on_delete=models.CASCADE)
    account = models.ForeignKey(Account,null=False,on_delete=models.CASCADE)
