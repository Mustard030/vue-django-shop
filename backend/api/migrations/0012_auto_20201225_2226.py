# Generated by Django 3.1.2 on 2020-12-25 22:26

import api.utils.changeName
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20201225_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsimage',
            name='image',
            field=models.ImageField(upload_to=api.utils.changeName.changeName),
        ),
    ]
