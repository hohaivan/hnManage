# Generated by Django 4.1.6 on 2023-05-28 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QLSanXuat', '0008_alter_cang_creator_alter_det_tay_cs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tay_in',
            name='CS',
            field=models.SmallIntegerField(default=1, editable=False, verbose_name='Tồn:'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tay_in',
            name='BatchID',
            field=models.CharField(blank=True, max_length=23, unique=True, verbose_name='Mã Lô:'),
        ),
        migrations.AlterField(
            model_name='tay_moc',
            name='BatchID',
            field=models.CharField(blank=True, max_length=23, unique=True, verbose_name='Mã Lô:'),
        ),
    ]
