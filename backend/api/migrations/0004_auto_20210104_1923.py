# Generated by Django 3.1.2 on 2021-01-04 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210104_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='path',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='路径'),
        ),
    ]
