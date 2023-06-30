# Generated by Django 4.1.6 on 2023-04-08 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yarn_manage', '0004_remove_delivery_batchid_remove_delivery_batchno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='PayValue',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, editable=False, max_digits=13),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='yarndebt_ly',
            name='Year',
            field=models.PositiveSmallIntegerField(default=2022),
        ),
    ]
