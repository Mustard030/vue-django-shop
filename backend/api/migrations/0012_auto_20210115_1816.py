# Generated by Django 3.1.2 on 2021-01-15 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20210115_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfo',
            name='introduce',
            field=models.TextField(blank=True, null=True, verbose_name='商品介绍'),
        ),
    ]