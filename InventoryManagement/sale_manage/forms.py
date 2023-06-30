from datetime import datetime
from django import forms
from .models import Sales, Returned, Customer_Pay, Customer_Debt


class DateInput(forms.DateInput):
    input_type = 'date'


class TextInput(forms.TextInput):
    input_type = 'text'


class HiddenFieldWidget(forms.HiddenInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_hidden'] = True
        return context


class sales_form(forms.ModelForm):
    Net = forms.CharField(label='Khối Lượng Bán:', required=False, disabled=True,
                                )
    PayAmount = forms.CharField(label='Tổng Thanh Toán:', required=False, disabled=True,
                                )

    class Meta:
        model = Sales
        fields = ['Date', 'PXK', 'Customer', 'Product_Name', 'Product_Type', 'Final_Product', 'Colours', 'Patterns', 'Qty', 'Weight', 'Cut',
                  'Price', 'Note', 'Creator', 'Net', 'PayAmount']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   'Colours': TextInput(attrs={'placeholder': 'ex: 19(4) 20(5)'}),
                   'Patterns': TextInput(attrs={'placeholder': 'ex: 3511(4) 3512(5)'}),
                   }


class returned_form(forms.ModelForm):
    Net = forms.CharField(label='Khối Lượng Bán:', required=False, disabled=True,
                          )
    PayAmount = forms.CharField(label='Tổng Thanh Toán:', required=False, disabled=True,
                                )

    class Meta:
        model = Returned
        fields = ['Date', 'Customer', 'Product_Name', 'Product_Type', 'Final_Product', 'Colours', 'Patterns',
                  'Qty', 'Weight', 'Cut',
                  'Price', 'Note', 'Creator', 'Net', 'PayAmount']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   'Colours': TextInput(attrs={'placeholder': 'ex: 19(4) 20(5)'}),
                   'Patterns': TextInput(attrs={'placeholder': 'ex: 3511(4) 3512(5)'}),
                   }


class customer_pay_form(forms.ModelForm):
    class Meta:
        model = Customer_Pay
        fields = ['Date', 'Customer', 'Amount', 'Note', 'Creator']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   }


class customer_debt_form(forms.ModelForm):
    class Meta:
        model = Customer_Debt
        fields = ['Customer', 'Year', 'Amount']