import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.validators import RegexValidator
from django.db import IntegrityError

# Create your models here.


def no_space_or_number_validator(value):
    if ' ' in value:
        raise ValidationError("Ký Hiệu Không Được Có Khoảng Trống")
    if any(char.isdigit() for char in value):
        raise ValidationError("Ký Hiệu Không Được Có Số")


class YarnVendor(models.Model):
    Name = models.CharField(max_length=20, unique=True, verbose_name='Tên NBH:')
    Code = models.PositiveSmallIntegerField(unique=True, validators=[MinValueValidator(1)], verbose_name='Mã NBH:')
    VendorCode = models.CharField(max_length=7, unique=True, blank=True, editable=False)
    Address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Địa Chỉ:')

    def save(self, *args, **kwargs):
        if self.Code < 10:
            self.VendorCode = f'V0{self.Code}'
        else:
            self.VendorCode = f'V{self.Code}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '1.1 NCC Sợi'

    def __str__(self):
        return f'{self.Name} - {self.VendorCode}'


class YarnType(models.Model):
    Name = models.CharField(max_length=20, unique=True, verbose_name='Loại Sợi:')

    def save(self, *args, **kwargs):
        if '  ' in self.Name:
            raise ValidationError('Chỉ Được Cách Tối Đa Một Khoảng Trắng Giữa Các Ký Tự')
        try:
            self.Name = self.Name.upper()  # Convert the value to uppercase
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError('Loại Sợi Này Đã Tồn Tại')

    class Meta:
        verbose_name_plural = '1.2 Loại Sợi'

    def __str__(self):
        return f'{self.Name}'


class Warehouse(models.Model):
    WH_choices = [('D', 'Dệt'), ('S', 'Se')]
    Name = models.CharField(max_length=20, unique=True, verbose_name='Địa Điểm:')
    Code = models.CharField(max_length=5, validators=[
        RegexValidator(regex=r'^[A-Za-z]*$', message="Chỉ Cho Phép Ký Tự Chữ Cái",
                       code='invalid_alpha'), no_space_or_number_validator], unique=True, verbose_name='Ký Hiệu:')
    Address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Địa Chỉ:')
    WH_Type = models.CharField(max_length=1, choices=WH_choices, verbose_name='Chức Năng:')

    class Meta:
        verbose_name_plural = '1.3 Kho Về Sợi'

    def __str__(self):
        return f'{self.Name}'


class Warehouse2(models.Model):
    Name = models.OneToOneField(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.Name}'


class YarnOrder(models.Model):
    Package_choice = [('T', 'Thùng'), ('K', 'Kiện'), ]
    Date = models.DateField(verbose_name='Ngày:')
    year = models.SmallIntegerField(editable=False)
    Vendor = models.ForeignKey(YarnVendor, on_delete=models.RESTRICT, verbose_name='Người Bán:')
    YarnType = models.ForeignKey(YarnType, on_delete=models.RESTRICT, verbose_name='Loại Sợi:')
    YarnStats = models.CharField(max_length=15, verbose_name='Chỉ Số Sợi:')
    YarnCode = models.CharField(max_length=10, null=True, blank=True, verbose_name='Mã Sợi:')
    Box_Pack = models.CharField(max_length=1, choices=Package_choice, verbose_name='Quy Cách:')
    BoxQty = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Số Thùng/Kiện:')
    Weight = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(1)],
                                 verbose_name='Khối Lượng:')
    Price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(1000)],
                                verbose_name='Đơn Giá:')
    BatchNo = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Số Lô:')
    BatchID = models.CharField(max_length=10, unique=True, blank=True, editable=False, verbose_name='Mã Lô:')
    Amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False, verbose_name='Thành Tiền:')
    Rest_B = models.SmallIntegerField(null=True, blank=True, editable=False, verbose_name='Số Th/K Còn Lại:')
    Rest_W = models.DecimalField(null=True, blank=True, editable=False, max_digits=9, decimal_places=2, verbose_name='Kh/Lượng Còn:')
    Note = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT, verbose_name='Người Tạo:')
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    @property
    def Total_Pay(self):
        return round(self.Weight * self.Price, 2)

    @property
    def rest_Box(self):
        if self.BoxQty is None:
            return None
        else:
            rows = Delivery.objects.filter(OrderID=self.id)
            Box_delivered = sum(row.BoxQty for row in rows)
            return self.BoxQty - Box_delivered

    @property
    def rest_Weight(self):
        rows = Delivery.objects.filter(OrderID=self.id)
        Weight_delivered = sum(row.Weight for row in rows)
        return self.Weight - Weight_delivered

    def save(self, *args, **kwargs):
        self.year = self.Date.year
        self.Amount = self.Total_Pay
        self.Rest_B = self.rest_Box
        self.Rest_W = self.rest_Weight
        self.BatchID = f'{self.year % 100}-{self.Vendor.VendorCode}L{self.BatchNo}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.BatchID}'

    class Meta:
        verbose_name_plural = '2.1 Đặt Sợi'

class Delivery(models.Model):
    class Meta:
        verbose_name_plural = '2.2 Giao Sợi'

    Date = models.DateField(verbose_name='Ngày:')
    year = models.PositiveSmallIntegerField(editable=False)
    OrderID = models.ForeignKey(YarnOrder, on_delete=models.CASCADE, verbose_name='Mã Đặt Sợi')
    YarnCode = models.CharField(max_length=10, null=True, blank=True, verbose_name='Mã Sợi:')
    BoxQty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Số Thùng/Kiện:')
    Weight = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(1)],
                                 verbose_name='Khối Lượng:')
    Price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(1000)], default='',
                                blank=True, verbose_name='Đơn Giá:')
    OtherCost = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], default='0',
                                    verbose_name='Chi Phí Khác:')
    PayValue = models.DecimalField(max_digits=13, decimal_places=2, editable=False, blank=True)
    Warehouse = models.ForeignKey(Warehouse, on_delete=models.RESTRICT, verbose_name='Kho:')
    Note = models.CharField(max_length=100, null=True, blank=True)
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT)
    Created_Time = models.DateTimeField(auto_now=True, editable=False)
    Sync = models.BooleanField(editable=False)

    @property
    def Total_Pay(self):
        return self.Weight * self.Price + self.OtherCost

    def get_default_YarnCode(self):
        return self.OrderID.YarnCode

    def get_default_Price(self):
        return self.OrderID.Price

    def save(self, Sync=True, *args, **kwargs):
        self.year = self.Date.year
        self.Sync = Sync
        self.PayValue = self.Weight * self.Price + self.OtherCost
        if not self.pk:
            self.YarnCode = self.get_default_YarnCode()
            self.Price = self.get_default_Price()
        super().save(*args, **kwargs)


class YarnTransfer(models.Model):
    Package_choice = [('T', 'Thùng'), ('K', 'Kiện'), ]

    Date = models.DateField(verbose_name='Ngày:')
    year = models.PositiveSmallIntegerField(editable=False)
    YarnType = models.ForeignKey(YarnType, on_delete=models.RESTRICT, verbose_name='Loại Sợi:')
    YarnStats = models.CharField(max_length=15, verbose_name='Chỉ Số Sợi:')
    YarnCode = models.CharField(max_length=10, null=True, blank=True, verbose_name='Mã Sợi:')
    Origin = models.ForeignKey(Warehouse2, on_delete=models.RESTRICT, null=True, verbose_name='Nơi Đi:')
    Destination = models.ForeignKey(Warehouse, on_delete=models.RESTRICT, verbose_name='Nơi Đến:')
    Box_Pack = models.CharField(max_length=1, null=True, blank=True, choices=Package_choice, verbose_name='Quy Cách:')
    BoxQty = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Số Thùng/Kiện:')
    Weight = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(1)],
                                 verbose_name='Khối Lượng:')
    Note = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT, verbose_name='Người Tạo:')
    Created_Time = models.DateTimeField(auto_now=True, editable=False)
    # signals fields
    Sync = models.BooleanField(editable=False)
    Database = models.CharField(max_length=10, editable=False, null=True)
    Address = models.BigIntegerField(editable=False, null=True)

    class Meta:
        verbose_name_plural = '2.3 Xuất Nhập Sợi'

    def clean(self):
        if self.Origin:
            if self.Destination.id == self.Origin.Name_id:
                raise ValidationError('Nơi Xuất và Nhập phải khác nhau')

    def save(self, Sync=False, Signal=False, *args, **kwargs):
        self.year = self.Date.year
        if self.pk:
            if self.Sync and not Signal:
                raise PermissionDenied('Không Cho Phép Sửa Dữ Liệu Đồng Bộ Từ Trang Này')
            else:
                self.Sync = Sync
                super().save(*args, **kwargs)
        else:
            self.Sync = Sync
            super().save(*args, **kwargs)

    def delete(self, Signal=False, *args, **kwargs):
        if self.Sync and not Signal:
            raise PermissionDenied('Không Cho Phép Xóa Dữ Liệu Đồng Bộ Từ Trang Này')
        else:
            super().delete(*args, **kwargs)


class YarnPay(models.Model):
    class Meta:
        verbose_name_plural = '2.4 Trả Tiền Sợi'

    Date = models.DateField(verbose_name='Ngày:')
    year = models.PositiveSmallIntegerField(editable=False)
    Vendor = models.ForeignKey(YarnVendor, on_delete=models.RESTRICT, verbose_name='Nhà Bán Hàng:')
    Pay = models.DecimalField(max_digits=13, decimal_places=2, validators=[MinValueValidator(1000)], verbose_name='Số Tiền Trả:')
    Deposit = models.DecimalField(max_digits=13, decimal_places=2, validators=[MinValueValidator(1000)], blank=True, null=True, verbose_name='Phần Cọc:')
    Batch = models.CharField(max_length=10, blank=True, null=True, verbose_name='Theo Lô Hàng:')
    Note = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT)
    Created_Time = models.DateTimeField(auto_now=True, editable=False)
    Sync = models.BooleanField(editable=False)

    def __str__(self):
        return f'{self.Date} - {self.Vendor.Name}'

    def save(self, Sync=True, *args, **kwargs):
        self.year = self.Date.year
        self.Sync = Sync
        super().save(*args, **kwargs)


class YarnDebt_LY(models.Model):
    Vendor = models.ForeignKey(YarnVendor, on_delete=models.RESTRICT, verbose_name='Người Bán:')
    Year = models.PositiveSmallIntegerField(default=datetime.datetime.now().year-1, verbose_name='Năm:')
    Debt = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Số Tiền:')
    Debt_LY = models.DecimalField(max_digits=14, decimal_places=2, editable=False, verbose_name='Nợ Năm Trước:')
    Buy_In = models.DecimalField(max_digits=14, decimal_places=2, editable=False, verbose_name='Mua Vào:')
    Pay_Out = models.DecimalField(max_digits=14, decimal_places=2, editable=False, verbose_name='Bán Ra:')
    Match = models.BooleanField()

    def save(self, *args, **kwargs):
        self.Debt_LY = self.Debt_LastYear
        self.Buy_In = self.Total_Buy
        self.Pay_Out = self.Total_Pay
        self.Match = self.Data_Match
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '2.5 Lưu Công Nợ Cuối Năm'
        unique_together = ['Vendor', 'Year']

    def clean(self):
        if self.Year > datetime.datetime.now().year:
            raise ValidationError(f'Chưa Thể Nhập Công Nợ Cho Năm {self.Year}')

    @property
    def Debt_LastYear(self):
        LastYear = YarnDebt_LY.objects.filter(Vendor=self.Vendor, Year=self.Year - 1)
        return sum(row.Debt for row in LastYear)

    @property
    def Total_Buy(self):
        Buy = Delivery.objects.filter(OrderID__Vendor=self.Vendor, year=self.Year)
        return sum(row.PayValue for row in Buy)

    @property
    def Total_Pay(self):
        Pay = YarnPay.objects.filter(Vendor=self.Vendor, year=self.Year)
        return sum(row.Pay for row in Pay)

    @property
    def Auto_Calculation(self):
        return self.Debt_LastYear + (self.Total_Buy - self.Total_Pay)

    @property
    def Data_Match(self):
        if self.Debt == self.Auto_Calculation:
            return True
        else:
            return False