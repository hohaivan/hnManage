# Generated by Django 4.1.6 on 2023-05-23 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yarn_manage', '0012_alter_yarntransfer_yarntype'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='Sync',
            field=models.BooleanField(default=True, editable=False),
            preserve_default=False,
        ),
    ]
