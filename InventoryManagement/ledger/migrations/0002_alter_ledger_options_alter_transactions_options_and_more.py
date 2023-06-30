# Generated by Django 4.1.6 on 2023-05-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ledger',
            options={'verbose_name_plural': '2. Sổ Cái'},
        ),
        migrations.AlterModelOptions(
            name='transactions',
            options={'verbose_name_plural': '1. Hạng Mục Giao Dịch'},
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='R_P',
            field=models.BooleanField(default=True, verbose_name='Thu:'),
        ),
    ]