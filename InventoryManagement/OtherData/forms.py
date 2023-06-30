from django import forms
from QLSanXuat.models import KhachHang, KhoDet, KhoTay, KhoIn, KhoNhuom, KhoCang, Product_class
from yarn_manage.models import YarnVendor, Warehouse, YarnType


class TextInput(forms.TextInput):
    input_type = 'text'


class Customer_form(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ['name', 'real_name', 'Phone_Number', 'Address', 'email', 'Own']


class KhoDet_form(forms.ModelForm):
    class Meta:
        model = KhoDet
        fields = ['KhoDet', 'KyHieu', 'Address', 'OS']


class KhoTay_form(forms.ModelForm):
    class Meta:
        model = KhoTay
        fields = ['KhoTay', 'KyHieu', 'Address', 'OS']


class KhoIn_form(forms.ModelForm):
    class Meta:
        model = KhoIn
        fields = ['KhoIn', 'KyHieu', 'Address', 'OS']


class KhoNhuom_form(forms.ModelForm):
    class Meta:
        model = KhoNhuom
        fields = ['KhoNhuom', 'KyHieu', 'Address', 'OS']
        

class KhoCang_form(forms.ModelForm):
    class Meta:
        model = KhoCang
        fields = ['KhoCang', 'KyHieu', 'Address', 'OS']


class ProductClass_form(forms.ModelForm):
    class Meta:
        model = Product_class
        fields = ['Product_class']


class YarnVendor_form(forms.ModelForm):
    class Meta:
        model = YarnVendor
        fields = ['Name', 'Code', 'Address']


class Warehouse_form(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['Name', 'Code', 'Address', 'WH_Type']


class YarnType_form(forms.ModelForm):
    class Meta:
        model = YarnType
        fields = ['Name']
