# Generated by Django 3.1.2 on 2020-12-04 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_deliveryinfo_userinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserInfo',
        ),
        migrations.RenameField(
            model_name='deliveryinfo',
            old_name='name',
            new_name='recipient',
        ),
        migrations.AddField(
            model_name='deliveryinfo',
            name='address',
            field=models.CharField(default='', max_length=128),
        ),
    ]