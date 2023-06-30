from datetime import datetime
from django import forms
from .models import ledger, Transactions


class DateInput(forms.DateInput):
    input_type = 'date'


class TextInput(forms.TextInput):
    input_type = 'text'


class ledger_form(forms.ModelForm):
    Transaction = forms.ModelChoiceField(queryset=Transactions.objects.filter(Auto_Sync=False),
                                         label='Hạng Mục Giao Dịch')

    class Meta:
        model = ledger
        fields = ['Date', 'Amount', 'Transaction', 'Description', 'Note', 'Creator']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}), }