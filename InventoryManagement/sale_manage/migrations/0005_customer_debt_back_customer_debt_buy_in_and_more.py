# Generated by Django 4.1.6 on 2023-06-01 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale_manage', '0004_alter_sales_pxk'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_debt',
            name='Back',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=14, verbose_name='Hàng Trả'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer_debt',
            name='Buy_In',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=14, verbose_name='Mua Vào'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer_debt',
            name='Debt_LY',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=14, verbose_name='Nợ Năm Trước'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer_debt',
            name='Pay_Out',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=14, verbose_name='Đã Thanh Toán'),
            preserve_default=False,
        ),
    ]
