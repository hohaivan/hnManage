import datetime
import re
from decimal import Decimal, ROUND_DOWN
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from QLSanXuat.models import KhachHang
# Create your models here.


class Sales(models.Model):
    FP_Choices = [('M', 'Mộc'), ('N', 'Nhuộm'), ('I', 'In')]

    Date = models.DateField(verbose_name='Ngày:')
    year = models.PositiveSmallIntegerField(editable=False)
    PXK = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)], verbose_name='Phiếu Xuất Kho:')
    Customer = models.ForeignKey(KhachHang, on_delete=models.RESTRICT, verbose_name='Khách Hàng:')
    Product_Name = models.CharField(max_length=20, verbose_name='Tên Hàng:')
    Product_Type = models.CharField(max_length=20, verbose_name='Loại Hàng:')
    Final_Product = models.CharField(max_length=1, choices=FP_Choices, verbose_name='Thành Phẩm:')
    Colours = models.CharField(max_length=100, blank=True, null=True, verbose_name='Mã Màu:')
    Patterns = models.CharField(max_length=100, blank=True, null=True, verbose_name='Mã Bông:')
    Qty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Số Cây:')
    Weight = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.1)], verbose_name='Khối Lượng:')
    Cut = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name='Trừ Đầu Cây:')
    Net_Weight = models.DecimalField(max_digits=7, decimal_places=2, editable=False, verbose_name='Khối Lượng Bán:')
    Price = models.PositiveIntegerField(validators=[MinValueValidator(1000)], verbose_name='Đơn Giá:')
    Amount = models.DecimalField(max_digits=13, decimal_places=2, editable=False, verbose_name='Thành Tiền:')
    Note = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT)
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = '1.1 Bán Hàng'

    def clean(self):
        if self.Final_Product == 'M':
            if self.Colours or self.Patterns:
                raise ValidationError('Colors and Patterns Codes are not allowed for this type of finished product')
        if self.Final_Product == 'N':
            if self.Patterns:
                raise ValidationError('Patterns Codes are not allowed for this type of finished product')
        if self.Final_Product == 'I':
            if self.Colours:
                raise ValidationError('Color Codes are not allowed for this type of finished product')
        if self.Colours and self.Patterns:
            raise ValidationError('Each Result cannot have both Color and Patterns')

        # check if the Qty in Patterns and Colours Code are numbers
        Colours_string = re.findall('\((.*?)\)', str(self.Colours))
        Patterns_string = re.findall('\((.*?)\)', str(self.Patterns))
        for i in range(0, len(Colours_string), 1):
            if Colours_string[i]:
                if float(Colours_string[i]) == 0 or not Colours_string[i].isdigit():
                    raise ValidationError('Please Check Your Color Codes Again')
            else:
                raise ValidationError('Please Check Your Color Codes Again')

        for i in range(0, len(Patterns_string), 1):
            if Patterns_string[i]:
                if float(Patterns_string[i]) == 0 or not Patterns_string[i].isdigit():
                    raise ValidationError('Please Check Your Pattern Codes Again')
            else:
                raise ValidationError('Please Check Your Pattern Codes Again')
        # end of checking

    def save(self, *args, **kwargs):
        self.year = self.Date.year
        self.Net_Weight = self.Weight - self.Cut
        self.Amount = self.Net_Weight * self.Price
        self.Amount = (self.Amount/1000).quantize(Decimal('1.'), rounding=ROUND_DOWN) * 1000
        super().save(*args, **kwargs)

    def Colours_display(self):
        if self.Colours:
            string = self.Colours.replace(' ', '_')
            parts = string.strip().split('_')
            if len(parts) < 4:
                return string
            else:
                for i in range(3, len(parts), 3):
                    parts[i] = ' ' + parts[i]
                return '_'.join(parts)

    def Patterns_display(self):
        if self.Patterns:
            string = self.Patterns.replace(' ', '_')
            parts = string.strip().split('_')
            if len(parts) < 4:
                return string
            else:
                for i in range(3, len(parts), 3):
                    parts[i] = ' ' + parts[i]
                return '_'.join(parts)


class Returned(models.Model):
    FP_Choices = [('M', 'Mộc'), ('N', 'Nhuộm'), ('I', 'In')]

    Date = models.DateField(verbose_name='Ngày:')
    year = models.PositiveSmallIntegerField(editable=False)
    Customer = models.ForeignKey(KhachHang, on_delete=models.RESTRICT, verbose_name='Khách Trả:')
    Product_Name = models.CharField(max_length=20, verbose_name='Tên Hàng:')
    Product_Type = models.CharField(max_length=20, verbose_name='Loại Hàng:')
    Final_Product = models.CharField(max_length=1, choices=FP_Choices, verbose_name='Thành Phẩm:')
    Colours = models.CharField(max_length=100, blank=True, null=True, verbose_name='Mã Màu:')
    Patterns = models.CharField(max_length=100, blank=True, null=True, verbose_name='Mã Bông:')
    Qty = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1)], verbose_name='Số Cây:')
    Weight = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.1)], verbose_name='Khối Lượng:')
    Cut = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name='Trừ Đầu Cây:')
    Net_Weight = models.DecimalField(max_digits=7, decimal_places=2, editable=False, verbose_name='Khối Lượng Bán:')
    Price = models.PositiveIntegerField(validators=[MinValueValidator(1000)], verbose_name='Đơn Giá:')
    Amount = models.DecimalField(max_digits=13, decimal_places=2, editable=False, verbose_name='Thành Tiền:')
    Note = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT)
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = '1.2 Hàng Khách Trả'

    def clean(self):
        if self.Final_Product == 'M':
            if self.Colours or self.Patterns:
                raise ValidationError('Colors and Patterns Codes are not allowed for this type of finished product')
        if self.Final_Product == 'N':
            if self.Patterns:
                raise ValidationError('Patterns Codes are not allowed for this type of finished product')
        if self.Final_Product == 'I':
            if self.Colours:
                raise ValidationError('Color Codes are not allowed for this type of finished product')
        if self.Colours and self.Patterns:
            raise ValidationError('Each Result cannot have both Color and Patterns')

        # check if the Qty in Patterns and Colours Code are numbers
        Colours_string = re.findall('\((.*?)\)', str(self.Colours))
        Patterns_string = re.findall('\((.*?)\)', str(self.Patterns))
        for i in range(0, len(Colours_string), 1):
            if Colours_string[i]:
                if float(Colours_string[i]) == 0 or not Colours_string[i].isdigit():
                    raise ValidationError('Kiểm Tra Lại Mã Màu')
            else:
                raise ValidationError('Kiểm Tra Lại Mã Màu')

        for i in range(0, len(Patterns_string), 1):
            if Patterns_string[i]:
                if float(Patterns_string[i]) == 0 or not Patterns_string[i].isdigit():
                    raise ValidationError('Kiểm Tra Lại Mã Bông')
            else:
                raise ValidationError('Kiểm Tra Lại Mã Bông')
        # end of checking

    def save(self, *args, **kwargs):
        self.year = self.Date.year
        self.Net_Weight = self.Weight - self.Cut
        self.Amount = self.Net_Weight * self.Price
        self.Amount = (self.Amount/1000).quantize(Decimal('1.'), rounding=ROUND_DOWN) * 1000
        super().save(*args, **kwargs)

    def Colours_display(self):
        if self.Colours:
            string = self.Colours.replace(' ', '_')
            parts = string.strip().split('_')
            if len(parts) < 4:
                return string
            else:
                for i in range(3, len(parts), 3):
                    parts[i] = ' ' + parts[i]
                return '_'.join(parts)

    def Patterns_display(self):
        if self.Patterns:
            string = self.Patterns.replace(' ', '_')
            parts = string.strip().split('_')
            if len(parts) < 4:
                return string
            else:
                for i in range(3, len(parts), 3):
                    parts[i] = ' ' + parts[i]
                return '_'.join(parts)


class Customer_Pay(models.Model):
    Date = models.DateField(verbose_name='Ngày:')
    year = models.PositiveSmallIntegerField(editable=False)
    Customer = models.ForeignKey(KhachHang, on_delete=models.RESTRICT, verbose_name='Khách Hàng:')
    Amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(1000)], verbose_name='Số Tiền Trả:')
    Sync = models.BooleanField(editable=False, verbose_name='Đồng Bộ')
    Note = models.CharField(blank=True, null=True, max_length=100, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT)
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = '1.3 Thanh Toán Của Khách'

    def save(self, Sync=True, *args, **kwargs):
        self.year = self.Date.year
        if Sync:
            self.Sync = True
        else:
            self.Sync = False
        super().save(*args, **kwargs)


class Customer_Debt(models.Model):
    Customer = models.ForeignKey(KhachHang, on_delete=models.RESTRICT, verbose_name='Khách Hàng')
    Year = models.PositiveSmallIntegerField(default=datetime.datetime.now().year-1, verbose_name='Năm')
    Amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Công Nợ')
    Debt_LY = models.DecimalField(max_digits=14, decimal_places=2, editable=False, verbose_name='Nợ Năm Trước')
    Buy_In = models.DecimalField(max_digits=14, decimal_places=2, editable=False, verbose_name='Mua Vào')
    Back = models.DecimalField(max_digits=14, decimal_places=2, editable=False, verbose_name='Hàng Trả')
    Pay_Out = models.DecimalField(max_digits=14, decimal_places=2, editable=False, verbose_name='Đã Thanh Toán')

    def save(self, *args, **kwargs):
        self.Debt_LY = self.Debt_LastYear
        self.Buy_In = self.Total_Buy
        self.Back = self.Total_Back
        self.Pay_Out = self.Total_Pay
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '1.4 Chốt Công Nợ Cuối Năm'
        unique_together = ['Customer', 'Year']

    def clean(self):
        if self.Year > datetime.datetime.now().year:
            raise ValidationError(f'Chưa Thể Nhập Công Nợ Cho Năm {self.Year}')

    @property
    def Debt_LastYear(self):
        LastYear = Customer_Debt.objects.filter(Customer=self.Customer, Year=self.Year - 1)
        return sum(row.Amount for row in LastYear) if LastYear.exists() else 0

    @property
    def Total_Buy(self):
        Buy = Sales.objects.filter(Customer=self.Customer, year=self.Year)
        return sum(row.Amount for row in Buy) if Buy.exists() else 0

    @property
    def Total_Back(self):
        Back = Returned.objects.filter(Customer=self.Customer, year=self.Year)
        return sum(row.Amount for row in Back) if Back.exists() else 0

    @property
    def Total_Pay(self):
        Pay = Customer_Pay.objects.filter(Customer=self.Customer, year=self.Year)
        return sum(row.Amount for row in Pay) if Pay.exists() else 0

    @property
    def Auto_Calculation(self):
        return self.Debt_LastYear + (self.Total_Buy - self.Total_Back - self.Total_Pay)

    @property
    def Data_Match(self):
        if self.Amount == self.Auto_Calculation:
            return True
        else:
            return False




