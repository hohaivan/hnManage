# Generated by Django 4.1.6 on 2023-06-21 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yarn_manage', '0019_yarndebt_ly_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yarnorder',
            name='Rest_B',
            field=models.SmallIntegerField(blank=True, editable=False, null=True, verbose_name='Số Th/K Còn Lại:'),
        ),
    ]