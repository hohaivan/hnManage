# Generated by Django 4.1.6 on 2023-05-26 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QLSanXuat', '0006_alter_det_tay_fromwhere'),
    ]

    operations = [
        migrations.AddField(
            model_name='det_tay',
            name='CS',
            field=models.SmallIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
    ]