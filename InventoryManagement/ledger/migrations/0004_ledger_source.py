# Generated by Django 4.1.6 on 2023-05-20 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0003_ledger_created_time_ledger_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='ledger',
            name='Source',
            field=models.CharField(blank=True, choices=[('Syn', 'Đồng Bộ'), ('Man', 'Thêm Mới')], max_length=3, verbose_name='Nguồn:'),
        ),
    ]
