from datetime import datetime
from django import forms
from .models import Det_Tay, Tay_Moc, Tay_In, Tay_Nhuom, Cang, KhoTay, KhoIn, KhoNhuom


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


class DetTay_form(forms.ModelForm):
    class Meta:
        model = Det_Tay
        fields = ['Date', 'Product_class', 'Product_name', 'M_per_kg', 'Fit_size', 'Spandex_rate', 'FromWhere', 'Destination', 'BatchNo',
                  'Quantity', 'Weight', 'RE', 'Note', 'User_Create']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}), }


class TayMoc_form(forms.ModelForm):
    FromWhere = forms.ModelChoiceField(
                            queryset=KhoTay.objects.all(),
                            label="Nơi Đi (Tẩy):",
                            to_field_name='KhoTay',
                            required=False)

    class Meta:
        model = Tay_Moc
        fields = ['Date', 'DetTay_ID', 'BatchID', 'BatchNo', 'Customer', 'FromWhere', 'Print_Des', 'Qty', 'Weight', 'Note', 'Creator']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}), }

    def __init__(self, *args, **kwargs):
        initial_foreign_key_value = kwargs.pop('initial_foreign_key_value')
        super(TayMoc_form, self).__init__(*args, **kwargs)
        self.fields['DetTay_ID'].initial = initial_foreign_key_value


class TayIn_form(forms.ModelForm):
    FromWhere = forms.ModelChoiceField(
                            queryset=KhoTay.objects.all(),
                            label="Nơi Đi (Tẩy):",
                            to_field_name='KhoTay',
                            required=False)

    class Meta:
        model = Tay_In
        fields = ['Date', 'DetTay_ID', 'BatchID', 'BatchNo', 'Customer', 'FromWhere', 'Print_Des', 'Qty', 'Weight', 'Note', 'Creator']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   'BatchID': TextInput(attrs={'disabled': True}),
                   }

    def __init__(self, *args, **kwargs):
        initial_foreign_key_value = kwargs.pop('initial_foreign_key_value')
        super(TayIn_form, self).__init__(*args, **kwargs)
        self.fields['DetTay_ID'].initial = initial_foreign_key_value


class TayNhuom_form(forms.ModelForm):
    FromWhere = forms.ModelChoiceField(
                            queryset=KhoTay.objects.all(),
                            label='Nơi Đi (Tẩy):',
                            to_field_name='KhoTay',
                            required=False)

    class Meta:
        model = Tay_Nhuom
        fields = ['Date', 'DetTay_ID', 'BatchID', 'BatchNo', 'Customer', 'FromWhere', 'Dye_Des', 'Qty', 'Weight', 'Note', 'Creator']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   'BatchID': TextInput(attrs={'disabled': True}),
                   }

    def __init__(self, *args, **kwargs):
        initial_foreign_key_value = kwargs.pop('initial_foreign_key_value')
        super(TayNhuom_form, self).__init__(*args, **kwargs)
        self.fields['DetTay_ID'].initial = initial_foreign_key_value


class In_Cang_form(forms.ModelForm):
    Print_Des = forms.ModelChoiceField(
                            queryset=KhoIn.objects.all(),
                            label='Nơi Đi (In):',
                            to_field_name='KhoIn',
                            required=False, )

    Code = forms.CharField(label='Mã Bông:', required=False)
    BatchID = forms.ModelChoiceField(
                            queryset=Cang.objects.all(),
                            label='Mã Lô:',
                            to_field_name='BatchID',
                            required=False, )

    class Meta:
        model = Cang
        fields = ['Date', 'Product_type', 'Print_ID', 'BatchID', 'BatchNo', 'Print_Des', 'Stretch_Des', 'Code', 'Qty', 'Weight', 'Note', 'Creator']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   'Product_type': TextInput(attrs={'disabled': True}),
                   }

    def __init__(self, *args, **kwargs):
        initial_foreign_key_value = kwargs.pop('initial_foreign_key_value')
        super(In_Cang_form, self).__init__(*args, **kwargs)
        self.fields['Print_ID'].initial = initial_foreign_key_value


class Nhuom_Cang_form(forms.ModelForm):
    Dye_Des = forms.ModelChoiceField(
                            queryset=KhoNhuom.objects.all(),
                            label='Nơi Đi (Nhuộm):',
                            to_field_name='KhoNhuom',
                            required=False, )
    Code = forms.CharField(label='Mã Màu:', required=False)
    BatchID = forms.ModelChoiceField(
                            queryset=Cang.objects.all(),
                            label='Mã Lô:',
                            to_field_name='BatchID',
                            required=False, )

    class Meta:
        model = Cang
        fields = ['Date', 'Product_type', 'Dye_ID', 'BatchID', 'BatchNo', 'Dye_Des', 'Stretch_Des', 'Code', 'Qty', 'Weight', 'Note', 'Creator']
        widgets = {'Date': DateInput(attrs={'max': datetime.now().date()}),
                   'Product_type': TextInput(attrs={'disabled': True}),
                   }

    def __init__(self, *args, **kwargs):
        initial_foreign_key_value = kwargs.pop('initial_foreign_key_value')
        super(Nhuom_Cang_form, self).__init__(*args, **kwargs)
        self.fields['Dye_ID'].initial = initial_foreign_key_value


