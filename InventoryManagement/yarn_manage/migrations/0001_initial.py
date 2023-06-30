# Generated by Django 4.1.6 on 2023-03-17 05:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30, unique=True, verbose_name='Kho Về Sợi')),
                ('Code', models.CharField(max_length=5, unique=True, verbose_name='Ký Hiệu')),
                ('Address', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': '1.3 Kho Về Sợi',
            },
        ),
        migrations.CreateModel(
            name='YarnType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=10, unique=True, verbose_name='Loại Sợi')),
            ],
            options={
                'verbose_name_plural': '1.2 Loại Sợi',
            },
        ),
        migrations.CreateModel(
            name='YarnVendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30, unique=True, verbose_name='Tên NBH')),
                ('Code', models.PositiveSmallIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Mã NBH')),
                ('VendorCode', models.CharField(blank=True, editable=False, max_length=7, unique=True)),
                ('Address', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': '1.1 NCC Sợi',
            },
        ),
        migrations.CreateModel(
            name='YarnOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(verbose_name='Ngày:')),
                ('year', models.SmallIntegerField(editable=False)),
                ('YarnStats', models.CharField(max_length=15, verbose_name='Chỉ Số Sợi:')),
                ('YarnCode', models.CharField(blank=True, max_length=10, null=True, verbose_name='Mã Sợi:')),
                ('Box_Pack', models.CharField(choices=[('T', 'Thùng'), ('K', 'Kiện')], max_length=1, verbose_name='Quy Cách:')),
                ('BoxQty', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Số Thùng/Kiện:')),
                ('Weight', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Khối Lượng:')),
                ('Price', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(1000)], verbose_name='Đơn Giá:')),
                ('BatchNo', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Số Lô:')),
                ('BatchID', models.CharField(blank=True, editable=False, max_length=10, unique=True, verbose_name='Mã Lô:')),
                ('Note', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ghi Chú:')),
                ('Created_Time', models.DateTimeField(auto_now=True)),
                ('Creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('Vendor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='yarn_manage.yarnvendor', verbose_name='Người Bán:')),
                ('YarnType', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='yarn_manage.yarntype', verbose_name='Loại Sợi:')),
            ],
            options={
                'verbose_name_plural': '2.1 Đặt Sợi',
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(verbose_name='Ngày:')),
                ('year', models.PositiveSmallIntegerField(editable=False)),
                ('YarnCode', models.CharField(blank=True, max_length=10, null=True, verbose_name='Mã Sợi:')),
                ('BoxQty', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Số Thùng/Kiện')),
                ('Weight', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Khối Lượng:')),
                ('Price', models.DecimalField(blank=True, decimal_places=2, default='', max_digits=9, validators=[django.core.validators.MinValueValidator(1000)], verbose_name='Đơn Giá:')),
                ('OtherCost', models.DecimalField(decimal_places=2, default='0', max_digits=9, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Chi Phí Khác:')),
                ('Note', models.CharField(blank=True, max_length=100, null=True)),
                ('Created_Time', models.DateTimeField(auto_now=True)),
                ('Creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('OrderID', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='yarn_manage.yarnorder', verbose_name='Mã Đặt Sợi')),
                ('Warehouse', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='yarn_manage.warehouse', verbose_name='Kho:')),
            ],
            options={
                'verbose_name_plural': '2.2 Giao Sợi',
            },
        ),
    ]
