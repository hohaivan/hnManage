# Generated by Django 4.1.6 on 2023-05-24 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yarn_manage', '0013_delivery_sync'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yarntransfer',
            name='Box_Pack',
            field=models.CharField(blank=True, choices=[('T', 'Thùng'), ('K', 'Kiện')], max_length=1, null=True, verbose_name='Quy Cách:'),
        ),
        migrations.AlterField(
            model_name='yarntransfer',
            name='Destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='yarn_manage.warehouse', verbose_name='Nhập Vào:'),
        ),
        migrations.AlterField(
            model_name='yarntransfer',
            name='Origin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='yarn_manage.warehouse2', verbose_name='Xuất Đi:'),
        ),
        migrations.AlterField(
            model_name='yarntype',
            name='Name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Loại Sợi:'),
        ),
    ]
