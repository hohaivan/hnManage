from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import PermissionDenied


# Create your models here.


class Transactions(models.Model):
    RP_Choices = [('Thu', 'Thu'), ('Chi', 'Chi')]
    Name = models.CharField(max_length=100, unique=True)
    R_P = models.CharField(max_length=3, choices=RP_Choices, verbose_name='Thu/Chi:')
    Auto_Sync = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Name}'

    class Meta:
        verbose_name_plural = '1. Hạng Mục Giao Dịch'


class ledger(models.Model):
    Date = models.DateField(verbose_name='Ngày Giao Dịch:')
    year = models.SmallIntegerField(editable=False)
    Amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.1)],
                                 verbose_name='Số Tiền:')
    Transaction = models.ForeignKey(Transactions, on_delete=models.RESTRICT, verbose_name='Hạng Mục Giao Dịch')
    Description = models.CharField(max_length=150, verbose_name='Diễn giải:')
    Note = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ghi Chú:')
    Sync = models.BooleanField(editable=False, verbose_name='Đồng Bộ:')
    Database = models.CharField(max_length=20, editable=False, null=True, verbose_name='Source:')
    Address = models.PositiveBigIntegerField(editable=False, null=True)
    Creator = models.ForeignKey(User, blank=True, on_delete=models.RESTRICT)
    Created_Time = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = '2. Sổ Cái'
        unique_together = ['Database', 'Address']

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




