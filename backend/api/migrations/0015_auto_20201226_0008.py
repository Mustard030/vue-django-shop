# Generated by Django 3.1.2 on 2020-12-26 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_goodsimage_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsimage',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
