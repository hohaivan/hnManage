# Generated by Django 4.1.6 on 2023-05-20 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QLSanXuat', '0003_alter_det_tay_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='det_tay',
            name='FromWhere',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='QLSanXuat.khodet', verbose_name='Nơi Đi:'),
        ),
    ]
