from django.contrib import admin
from .models import YarnType, YarnOrder, Warehouse, YarnVendor, Delivery, YarnPay, YarnDebt_LY, YarnTransfer


class YarnOrderAdmin(admin.ModelAdmin):
    list_display = ('Date', 'BatchID', 'BoxQty', 'Box_Pack', 'Weight', 'Price')


class YarnTransferAdmin(admin.ModelAdmin):
    list_display = ('Date', 'YarnType', 'Origin', 'Destination', 'Weight', 'Sync', 'Database', 'Address')


class YarnPayAdmin(admin.ModelAdmin):
    list_display = ('Date', 'Vendor', 'Pay', 'Deposit', 'Batch', 'Note')


class YarnDebt_LYAdmin(admin.ModelAdmin):
    list_display = ('Vendor', 'Year', 'Debt', 'Auto_Calculation')


# Register your models here.
admin.site.register(YarnType)
admin.site.register(YarnVendor)
admin.site.register(YarnOrder, YarnOrderAdmin)
admin.site.register(Warehouse)
admin.site.register(Delivery)
admin.site.register(YarnTransfer, YarnTransferAdmin)
admin.site.register(YarnPay, YarnPayAdmin)
admin.site.register(YarnDebt_LY, YarnDebt_LYAdmin)



