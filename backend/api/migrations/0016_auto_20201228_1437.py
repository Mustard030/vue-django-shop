# Generated by Django 3.1.2 on 2020-12-28 14:37

import api.utils.changeName
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20201226_0008'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=api.utils.changeName.changeTempName)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='introduce',
            field=models.TextField(blank=True, null=True),
        ),
    ]
