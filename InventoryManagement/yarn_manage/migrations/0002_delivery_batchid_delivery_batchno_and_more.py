# Generated by Django 4.1.6 on 2023-03-17 08:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yarn_manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='BatchID',
            field=models.CharField(blank=True, editable=False, max_length=13, unique=True, verbose_name='Mã Lô:'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='BatchNo',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Lần Giao:'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='BoxQty',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Số Thùng/Kiện:'),
        ),
    ]