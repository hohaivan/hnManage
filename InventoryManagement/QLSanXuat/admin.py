from django.contrib import admin
from .models import KhoDet, KhoTay, KhoIn, KhoNhuom, KhoCang, Product_class, Det_Tay, KhachHang, Tay_Moc, Tay_In, Tay_Nhuom, Cang


class Det_TayAdmin(admin.ModelAdmin):
    list_display = ('BatchID', 'Product_class', 'Product_name', 'Quantity', 'Weight', 'current_stock')


# Register your models here.


admin.site.register(KhoDet)
admin.site.register(KhoTay)
admin.site.register(KhoIn)
admin.site.register(KhoNhuom)
admin.site.register(KhoCang)
admin.site.register(Det_Tay, Det_TayAdmin)
admin.site.register(Product_class)
admin.site.register(KhachHang)
admin.site.register(Tay_Moc)
admin.site.register(Tay_In)
admin.site.register(Tay_Nhuom)
admin.site.register(Cang)
