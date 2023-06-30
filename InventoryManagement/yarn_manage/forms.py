from datetime import datetime
from django import forms
from .models import YarnOrder, Delivery, YarnPay, YarnTransfer, YarnDebt_LY


class DateInput(forms.DateInput):
    input_type = 'date'


class TextInput(forms.TextInput):
    input_type = 'text'


class YarnOrder_form(forms.ModelForm):
    PayAmount = forms.CharField(label='Tổng Thanh Toán:', required=False, disabled=True,)

    class Meta:
        model = YarnOrder
        fields = ['Date', 'Vendor', 'YarnType', 'YarnStats', 'YarnCode', 'Box_Pack', 'BoxQty', 'Weight', 'Price',
                  'PayAmount', 'BatchNo', 'Note', 'Creator']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   }

    def clean(self):
        cleaned_data = super().clean()
        Weight = cleaned_data.get('Weight')
        Price = cleaned_data.get('Price')
        if Weight is not None and Price is not None:
            cleaned_data['PayAmount'] = Weight * Price
        return cleaned_data


class Delivery_form(forms.ModelForm):
    PayAmount = forms.CharField(label='Tổng Thanh Toán:', required=False, disabled=True,)
    Box_Pack = forms.CharField(max_length=5, label='Quy Cách:', required=False, disabled=True)
    OrderID = forms.ModelChoiceField(queryset=YarnOrder.objects.all(), label='Mã Đặt Sợi:', disabled=True)
    Vendor = forms.CharField(label='Người Bán', required=False, disabled=True)
    VendorCode = forms.CharField(label='Mã NB:', required=False,  disabled=True)
    YarnType = forms.CharField(label='Loại Sợi:', required=False, disabled=True)
    YarnStats = forms.CharField(label='Chỉ Số:', required=False, disabled=True)

    class Meta:
        model = Delivery
        fields = ['Date', 'OrderID', 'YarnCode', 'BoxQty', 'Weight', 'Price', 'OtherCost', 'Warehouse', 'Note', 'Creator',
                  'PayAmount', 'Box_Pack', 'Vendor', 'VendorCode', 'YarnType', 'YarnStats']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   }

    def __init__(self, *args, **kwargs):
        initial_foreign_key_value = kwargs.pop('initial_foreign_key_value')
        super(Delivery_form, self).__init__(*args, **kwargs)
        self.fields['OrderID'].initial = initial_foreign_key_value


class YarnTransfer_form(forms.ModelForm):
    class Meta:
        model = YarnTransfer
        fields = ['Date', 'YarnType', 'YarnStats', 'YarnCode', 'Box_Pack', 'BoxQty', 'Weight', 'Origin', 'Destination',  'Note',
                  'Creator', ]
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   }


class YarnPay_form(forms.ModelForm):
    class Meta:
        model = YarnPay
        fields = ['Date', 'Vendor', 'Pay', 'Deposit', 'Batch', 'Note', 'Creator']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   }


class YarnDebt_form(forms.ModelForm):
    class Meta:
        model = YarnDebt_LY
        fields = ['Vendor', 'Year', 'Debt']