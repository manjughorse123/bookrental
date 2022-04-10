from django.contrib import admin
from transactions.models import Transactions


class TransactionAdmin(admin.ModelAdmin):
	list_display = ['transaction' ,'transaction_date' ,'status' ,'customer' ,'order']
	

admin.site.register(Transactions, TransactionAdmin)