from django.contrib import admin
from .models import Customer,Loan, Account,Transaction, Setting


# Register your models here.

admin.site.register(Customer)
admin.site.register(Loan)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Setting)
