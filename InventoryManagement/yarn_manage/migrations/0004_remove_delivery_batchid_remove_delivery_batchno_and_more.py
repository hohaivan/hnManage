# Generated by Django 4.1.6 on 2023-04-08 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yarn_manage', '0003_alter_delivery_orderid_alter_warehouse_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='BatchID',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='BatchNo',
        ),
        migrations.CreateModel(
            name='YarnDebt_LY',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Year', models.PositiveSmallIntegerField(default=2023)),
                ('Debt', models.DecimalField(decimal_places=2, max_digits=14)),
                ('Vendor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='yarn_manage.yarnvendor')),
            ],
            options={
                'verbose_name_plural': 'Lưu Công Nợ Cuối Năm',
                'unique_together': {('Vendor', 'Year')},
            },
        ),
    ]