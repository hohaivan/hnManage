from django.contrib import admin
from .models import Sales, Returned, Customer_Pay, Customer_Debt


class SalesAdmin(admin.ModelAdmin):
    list_display = ('Date', 'PXK', 'Customer', 'Product_Name', 'Product_Type', 'Final_Product', 'Colours', 'Patterns',\
                    'Qty', 'Net_Weight', 'Price', 'Amount')


class ReturnedAdmin(admin.ModelAdmin):
    list_display = ('Date', 'Customer', 'Product_Name', 'Product_Type', 'Final_Product', 'Colours', 'Patterns',\
                    'Qty', 'Net_Weight', 'Price', 'Amount')


class Customer_PayAdmin(admin.ModelAdmin):
    list_display = ('Date', 'year', 'Amount', 'Note')


class Customer_DebtAdmin(admin.ModelAdmin):
    list_display = ('Customer', 'Year', 'Amount', 'Auto_Calculation', 'Total_Buy', 'Total_Back', 'Total_Pay')


# Register your models here.
admin.site.register(Sales, SalesAdmin)
admin.site.register(Returned, ReturnedAdmin)
admin.site.register(Customer_Debt, Customer_DebtAdmin)
admin.site.register(Customer_Pay, Customer_PayAdmin)