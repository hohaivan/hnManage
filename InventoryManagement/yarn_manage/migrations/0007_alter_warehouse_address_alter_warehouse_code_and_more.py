# Generated by Django 4.1.6 on 2023-05-19 07:56

import django.core.validators
from django.db import migrations, models
import yarn_manage.models


class Migration(migrations.Migration):

    dependencies = [
        ('yarn_manage', '0006_alter_yarndebt_ly_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='Address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Địa Chỉ:'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='Code',
            field=models.CharField(max_length=5, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_alpha', message='Chỉ Cho Phép Ký Tự Chữ Cái', regex='^[A-Za-z]*$'), yarn_manage.models.no_space_or_number_validator], verbose_name='Ký Hiệu:'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='Name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Địa Điểm:'),
        ),
        migrations.AlterField(
            model_name='yarntype',
            name='Name',
            field=models.CharField(max_length=10, unique=True, verbose_name='Thêm Loại Sợi Mới:'),
        ),
        migrations.AlterField(
            model_name='yarnvendor',
            name='Address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Địa Chỉ:'),
        ),
        migrations.AlterField(
            model_name='yarnvendor',
            name='Code',
            field=models.PositiveSmallIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Mã NBH:'),
        ),
        migrations.AlterField(
            model_name='yarnvendor',
            name='Name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Tên NBH:'),
        ),
    ]
