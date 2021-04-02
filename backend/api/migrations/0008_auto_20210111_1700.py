# Generated by Django 3.1.2 on 2021-01-11 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210105_2359'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TempImage',
        ),
        migrations.AlterField(
            model_name='goodsimage',
            name='itemID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.goodsinfo', verbose_name='归属商品'),
        ),
    ]