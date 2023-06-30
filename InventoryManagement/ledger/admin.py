from django.contrib import admin
from .models import Transactions, ledger


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id','Name', 'R_P')


# Register your models here.

admin.site.register(Transactions, TransactionsAdmin)
admin.site.register(ledger)
