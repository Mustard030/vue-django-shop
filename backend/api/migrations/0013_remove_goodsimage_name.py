# Generated by Django 3.1.2 on 2020-12-25 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20201225_2226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodsimage',
            name='name',
        ),
    ]
