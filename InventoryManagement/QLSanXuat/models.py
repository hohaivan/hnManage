from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import IntegrityError
from phone_field import PhoneField


# Sub models From Here

def no_space_or_number_validator(value):
    if ' ' in value:
        raise ValidationError("Ký Hiệu Không Được Có Khoảng Trống")
    if any(char.isdigit() for char in value):
        raise ValidationError("Ký Hiệu Không Được Có Số")


class KhoDet(models.Model):
    KhoDet = models.CharField(max_length=30, unique=True, verbose_name='Tên Xưởng:')
    KyHieu = models.CharField(max_length=5, validators=[
        RegexValidator(regex=r'^[A-Za-z]*$', message="Chỉ Cho Phép Kí Tự Chữ Cái.",
                       code='invalid_alpha'), no_space_or_number_validator], unique=True, verbose_name='Ký Hiệu:')
    Address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Địa Chỉ:')
    OS = models.BooleanField(default=1, verbose_name='Gia Công')

    def __str__(self):
        return f'{self.KhoDet}'

    class Meta:
        verbose_name_plural = '2.1. Xưởng Dệt'


class KhoTay(models.Model):
    KhoTay = models.CharField(max_length=30, unique=True, verbose_name='Lò Tẩy')
    KyHieu = models.CharField(max_length=5, validators=[
        RegexValidator(regex=r'^[A-Za-z]*$', message="Chỉ Cho Phép Kí Tự Chữ Cái.",
                       code='invalid_alpha'), no_space_or_number_validator], unique=True, verbose_name='Ký Hiệu:')
    Address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Địa Chỉ')
    OS = models.BooleanField(default=1, verbose_name='Gia Công')

    def __str__(self):
        return f'{self.KhoTay}'

    class Meta:
        verbose_name_plural = '2.4. Lò Tẩy'


class Product_class(models.Model):
    Product_class = models.CharField(max_length=20, unique=True, verbose_name='Phân Loại Hàng:')

    def save(self, *args, **kwargs):
        if '  ' in self.Product_class:
            raise ValidationError('Chỉ Được Cách Tối Đa Một Khoảng Trắng Giữa Các Ký Tự')
        try:
            self.Product_class = self.Product_class.upper()  # Convert the value to uppercase
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError('Phân Loại Hàng Này Đã Tồn Tại')

    def __str__(self):
        return f'{self.Product_class}'

    class Meta:
        verbose_name_plural = '2.2. Phân Loại Hàng'


class KhachHang(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Tên Khách Hàng:')
    real_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Tên Khác:')
    Phone_Number = PhoneField(null=True, blank=True, verbose_name='Số ĐT:')
    Address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Địa Chỉ:')
    email = models.EmailField(null=True, blank=True, verbose_name='Email:')
    Own = models.BooleanField(default=False, verbose_name='Nội Bộ')

    class Meta:
        verbose_name_plural = '2.3. Khách Hàng'

    def __str__(self):
        return f'{self.name}'


class KhoIn(models.Model):
    KhoIn = models.CharField(max_length=20, unique=True, verbose_name='Lò In')
    KyHieu = models.CharField(max_length=5, validators=[
        RegexValidator(regex=r'^[A-Za-z]*$', message="Chỉ Cho Phép Kí Tự Chữ Cái.",
                       code='invalid_alpha'), no_space_or_number_validator], unique=True, verbose_name='Ký Hiệu:')
    Address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Địa Chỉ')
    OS = models.BooleanField(default=1, verbose_name='Gia Công')

    class Meta:
        verbose_name_plural = '2.5. Lò In'

    def __str__(self):
        return f'{self.KhoIn}'


class KhoNhuom(models.Model):
    KhoNhuom = models.CharField(max_length=20, unique=True, verbose_name='Lò Nhuộm')
    KyHieu = models.CharField(max_length=5, validators=[
        RegexValidator(regex=r'^[A-Za-z]*$', message="Chỉ Cho Phép Kí Tự Chữ Cái.",
                       code='invalid_alpha'), no_space_or_number_validator], unique=True, verbose_name='Ký Hiệu:')
    Address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Địa Chỉ')
    OS = models.BooleanField(default=1, verbose_name='Gia Công')

    class Meta:
        verbose_name_plural = '2.6. Lò Nhuộm'

    def __str__(self):
        return f'{self.KhoNhuom}'


class KhoCang(models.Model):
    KhoCang = models.CharField(max_length=20, unique=True, verbose_name='Lò Căng')
    KyHieu = models.CharField(max_length=5, validators=[
        RegexValidator(regex=r'^[A-Za-z]*$', message="Only alphabetic characters are allowed.",
                       code='invalid_alpha'), no_space_or_number_validator], unique=True, verbose_name='Ký Hiệu:')
    Address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Địa Chỉ')
    OS = models.BooleanField(default=1, verbose_name='Gia Công')

    class Meta:
        verbose_name_plural = '2.7. Lò Căng'

    def __str__(self):
        return f'{self.KhoCang}'


# Main models From Here
class Det_Tay(models.Model):
    Date = models.DateField(verbose_name='Ngày:')
    year = models.SmallIntegerField(editable=False)
    Product_class = models.ForeignKey(Product_class, on_delete=models.RESTRICT, verbose_name='Phân Loại:')
    Product_name = models.CharField(max_length=20, verbose_name='Tên Hàng:')
    M_per_kg = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True, verbose_name='Số m/kg:')
    Fit_size = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True, verbose_name='Khổ Hàng:')
    Spandex_rate = models.DecimalField(max_digits=3, decimal_places=1, validators=[MaxValueValidator(100)], blank=True,
                                       null=True, verbose_name='% Spandex:')
    FromWhere = models.ForeignKey(KhoDet, null=True, on_delete=models.RESTRICT, verbose_name='Nơi Đi:')
    Destination = models.ForeignKey(KhoTay, on_delete=models.RESTRICT, verbose_name='Nơi Đến:')
    BatchNo = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(1)],
                                  verbose_name='Mã Lô:')
    BatchID = models.CharField(max_length=20, unique=True, editable=False, verbose_name='Mã Lô')
    Quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Số Lượng (Cây):')
    Weight = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.1)],
                                 verbose_name='Khối Lượng:')
    CS = models.SmallIntegerField(editable=False, verbose_name='Tồn:')
    Note = models.CharField(max_length=100, blank=True, verbose_name='Ghi Chú:')
    RE = models.BooleanField(default=False, verbose_name='Hàng Trả')
    User_Create = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT)
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    @property
    def current_stock(self):
        TayMoc_units = Tay_Moc.objects.filter(DetTay_ID=self.id)
        sold_units = sum(row.Qty for row in TayMoc_units)

        TayIn_units = Tay_In.objects.filter(DetTay_ID=self.id)
        Print_units = sum(row.Qty for row in TayIn_units)

        TayNhuom_units = Tay_Nhuom.objects.filter(DetTay_ID=self.id)
        Dye_units = sum(row.Qty for row in TayNhuom_units)
        return self.Quantity - sold_units - Print_units - Dye_units

    class Meta:
        unique_together = [['year', 'FromWhere', 'Destination', 'BatchNo', 'RE']]
        verbose_name_plural = '1.1. Dệt Tẩy'

    def __str__(self):
        return f'{self.BatchID}'

    def save(self, admin=True, *args, **kwargs):
        self.year = self.Date.year
        self.CS = self.current_stock
        if self.BatchNo / int(self.BatchNo) == 1:
            a = int(self.BatchNo)
            if a < 10:
                a = '0' + str(a)
        else:
            a = self.BatchNo
        if self.RE == 0:
            self.BatchID = f'{self.year % 100}-{self.FromWhere.KyHieu}{a}{self.Destination.KyHieu}'
        else:
            self.FromWhere = None
            self.BatchID = f'(HT)-{self.year % 100}-{a}{self.Destination.KyHieu}'

        if self.CS >= 0:
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Vượt Ngưỡng Tồn Kho')


class Tay_Moc(models.Model):
    Date = models.DateField(verbose_name='Ngày:')
    year = models.SmallIntegerField(editable=False)
    DetTay_ID = models.ForeignKey(Det_Tay, on_delete=models.CASCADE, verbose_name='Mã Lô Dệt Tẩy:')
    BatchNo = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Lần Xuất:')
    BatchID = models.CharField(max_length=23, unique=True, blank=True, verbose_name='Mã Lô:')
    Customer = models.ForeignKey(KhachHang, on_delete=models.RESTRICT, limit_choices_to={'Own': False},
                                 verbose_name='Khách Hàng:')
    Print_Des = models.ForeignKey(KhoIn, on_delete=models.RESTRICT, verbose_name='Nơi Đến (In):')
    Qty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Số Lượng (Cây):')
    Weight = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.1)],
                                 verbose_name='Khối Lượng:')
    Note = models.CharField(max_length=100, blank=True, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT, verbose_name='Người Tạo:')
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    def save(self, admin=True, *args, **kwargs):
        self.year = self.Date.year
        self.BatchID = f'{self.DetTay_ID.BatchID}-R{str(self.BatchNo)}'
        if admin:
            if self.DetTay_ID.current_stock < self.Qty:
                raise ValidationError('Lỗi: Số Lượng Vượt Quá Hàng Tồn Còn Lại')
        super(Tay_Moc, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '1.2. Tẩy Mộc'

    def __str__(self):
        return f'{self.Customer} - {self.BatchID}'


class Tay_In(models.Model):
    Date = models.DateField(verbose_name='Ngày:')
    year = models.SmallIntegerField(editable=False)
    DetTay_ID = models.ForeignKey(Det_Tay, on_delete=models.CASCADE, verbose_name='Mã Lô Dệt Tẩy:')
    BatchNo = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Lần Xuất:')
    BatchID = models.CharField(max_length=23, unique=True, blank=True, verbose_name='Mã Lô:')
    Customer = models.ForeignKey(KhachHang, on_delete=models.RESTRICT, limit_choices_to={'Own': True},
                                 verbose_name='Khách Hàng:')
    Print_Des = models.ForeignKey(KhoIn, on_delete=models.RESTRICT, verbose_name='Lò In:')
    Qty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Số Lượng (Cây):')
    Weight = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.1)],
                                 verbose_name='Khối Lượng:')
    CS = models.SmallIntegerField(editable=False, verbose_name='Tồn:')
    Note = models.CharField(max_length=100, blank=True, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT, verbose_name='Người Tạo:')
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    @property
    def current_stock(self):
        Cang_rows = Cang.objects.filter(Print_ID=self.id)
        Cang_units = sum(row.Qty for row in Cang_rows)
        return self.Qty - Cang_units

    def save(self, admin=True, *args, **kwargs):
        self.year = self.Date.year
        if not self.pk:
            self.CS = self.Qty
        else:
            self.CS = self.current_stock
        self.BatchID = f'{self.DetTay_ID.BatchID}-P{self.BatchNo}'
        if self.CS >= 0:
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Vượt Ngưỡng Tồn Kho')

    class Meta:
        verbose_name_plural = '1.3. Tẩy In'

    def __str__(self):
        return self.BatchID


class Tay_Nhuom(models.Model):
    Date = models.DateField(verbose_name='Ngày:')
    year = models.SmallIntegerField(editable=False)
    DetTay_ID = models.ForeignKey(Det_Tay, on_delete=models.CASCADE, verbose_name='Mã Lô Dệt Tẩy:')
    BatchNo = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Lần Xuất:')
    BatchID = models.CharField(max_length=23, unique=True, blank=True, verbose_name='Mã Lô')
    Customer = models.ForeignKey(KhachHang, on_delete=models.RESTRICT, limit_choices_to={'Own': True},
                                 verbose_name='Khách Hàng:')
    Dye_Des = models.ForeignKey(KhoNhuom, on_delete=models.RESTRICT, verbose_name='Lò Nhuộm:')
    Qty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Số Lượng (Cây):')
    Weight = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.1)],
                                 verbose_name='Khối Lượng:')
    CS = models.SmallIntegerField(editable=False, verbose_name='Tồn:')
    Note = models.CharField(max_length=100, blank=True, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT, verbose_name='Người Tạo:')
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    @property
    def current_stock(self):
        Cang_rows = Cang.objects.filter(Dye_ID=self.id)
        Cang_units = sum(row.Qty for row in Cang_rows)
        return self.Qty - Cang_units

    def save(self, admin=True, *args, **kwargs):
        self.year = self.Date.year
        if not self.pk:
            self.CS = self.Qty
        else:
            self.CS = self.current_stock
        self.BatchID = f'{self.DetTay_ID.BatchID}-D{self.BatchNo}'
        if self.CS >= 0:
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Vượt Ngưỡng Tồn Kho')

    class Meta:
        verbose_name_plural = '1.4. Tẩy Nhuộm'

    def __str__(self):
        return self.BatchID


class Cang(models.Model):
    type_choices = [('P', 'In'), ('D', 'Nhuộm'), ]

    Date = models.DateField(verbose_name='Ngày:')
    year = models.PositiveSmallIntegerField(editable=False)
    Product_class = models.CharField(max_length=20, editable=False, verbose_name='Loại Hàng')    # save product class again
    Product_name = models.CharField(max_length=20, editable=False, verbose_name='Tên Hàng')     # save product name again
    Product_type = models.CharField(max_length=1, blank=True, choices=type_choices, verbose_name='Loại Thành Phẩm:')
    Print_ID = models.ForeignKey(Tay_In, on_delete=models.CASCADE, related_name='Print_Dye', null=True, blank=True, verbose_name='Mã Lô In')
    Dye_ID = models.ForeignKey(Tay_Nhuom, on_delete=models.CASCADE, related_name='Print_Dye', null=True, blank=True, verbose_name='Mã Lô Nhuộm:')
    Customer = models.CharField(max_length=30, null=True, blank=True, editable=False)
    BatchNo = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Lần Xuất:')
    BatchID = models.CharField(max_length=26, unique=True, blank=True, verbose_name='Mã Lô')
    Stretch_Des = models.ForeignKey(KhoCang, on_delete=models.RESTRICT, verbose_name='Lò Căng:')
    Code = models.CharField(max_length=20, null=True, blank=True, verbose_name='Mã Màu/ Mã Bông:')
    uCode = models.CharField(max_length=22, editable=False, verbose_name='MM/MB')
    Qty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Số Lượng (Cây):')
    Weight = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.1)],
                                 verbose_name='Khối Lượng:')
    Note = models.CharField(max_length=100, blank=True, verbose_name='Ghi Chú:')
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT, verbose_name='Người Tạo:')
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    def clean(self):
        if self.Print_ID and self.Dye_ID:
            raise ValidationError('Just Print_ID or Dye_ID, not both')
        if self.Print_ID is None and self.Dye_ID is None:
            raise ValidationError('At Least Need to Fill Print_ID or Dye_ID')
        if self.Product_type == 'P' and self.Dye_ID:
            raise ValidationError('Wrong Type, Please Provide Print_ID')
        if self.Product_type == 'D' and self.Print_ID:
            raise ValidationError('Wrong Type, Please Provide Dye_ID')

    class Meta:
        verbose_name_plural = '1.5. Căng'

    def __str__(self):
        return self.BatchID

    def save(self, admin=True, *args, **kwargs):
        self.year = self.Date.year
        if self.Product_type == 'P':
            self.Product_class = self.Print_ID.DetTay_ID.Product_class.Product_class
            self.Product_name = self.Print_ID.DetTay_ID.Product_name
            self.BatchID = f'{self.Print_ID.BatchID}-S{self.BatchNo}'
            self.uCode = f'B-{self.Code}'
            if not self.pk:
                self.Customer = self.Print_ID.Customer
        elif self.Product_type == 'D':
            self.Product_class = self.Dye_ID.DetTay_ID.Product_class.Product_class
            self.Product_name = self.Dye_ID.DetTay_ID.Product_name
            self.BatchID = f'{self.Dye_ID.BatchID}-S{self.BatchNo}'
            self.uCode = f'M-{self.Code}'
            if not self.pk:
                self.Customer = self.Dye_ID.Customer

        super().save(*args, **kwargs)
