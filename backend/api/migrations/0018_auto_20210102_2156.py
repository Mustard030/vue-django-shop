# Generated by Django 3.1.2 on 2021-01-02 21:56

import api.utils.changeName
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0017_auto_20201230_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryinfo',
            name='province',
            field=models.CharField(default='', max_length=30, verbose_name='省市'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='childrenmenu',
            name='authName',
            field=models.CharField(max_length=20, verbose_name='子菜单名'),
        ),
        migrations.AlterField(
            model_name='childrenmenu',
            name='parentMenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.menu', verbose_name='父菜单'),
        ),
        migrations.AlterField(
            model_name='childrenmenu',
            name='path',
            field=models.CharField(max_length=128, verbose_name='路径'),
        ),
        migrations.AlterField(
            model_name='deliveryinfo',
            name='address',
            field=models.CharField(default='', max_length=128, verbose_name='详细地址'),
        ),
        migrations.AlterField(
            model_name='deliveryinfo',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='deliveryinfo',
            name='recipient',
            field=models.CharField(max_length=10, verbose_name='收件人姓名'),
        ),
        migrations.AlterField(
            model_name='deliveryinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='归属用户'),
        ),
        migrations.AlterField(
            model_name='goodsimage',
            name='image',
            field=models.ImageField(upload_to=api.utils.changeName.changeName, verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='goodsimage',
            name='itemID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.goodsinfo', verbose_name='归属商品'),
        ),
        migrations.AlterField(
            model_name='goodsimage',
            name='name',
            field=models.CharField(max_length=255, verbose_name='图片名'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='introduce',
            field=models.TextField(blank=True, null=True, verbose_name='商品介绍'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='itemClass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.goodskind', verbose_name='商品种类'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='itemName',
            field=models.CharField(max_length=100, verbose_name='商品名'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='merchantId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.merchant', verbose_name='归属商家'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='reserve',
            field=models.IntegerField(default=0, verbose_name='库存'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='sales',
            field=models.IntegerField(default=0, verbose_name='销量'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='unit',
            field=models.CharField(max_length=5, verbose_name='单位'),
        ),
        migrations.AlterField(
            model_name='goodskind',
            name='name',
            field=models.CharField(max_length=10, verbose_name='商品种类名称'),
        ),
        migrations.AlterField(
            model_name='goodskind',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.goodskind', verbose_name='父类商品种类'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='authName',
            field=models.CharField(max_length=10, verbose_name='菜单名'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='path',
            field=models.CharField(max_length=128, verbose_name='路径'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='管理员'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='merchantName',
            field=models.CharField(max_length=30, verbose_name='商家名称'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='deliveryInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.deliveryinfo', verbose_name='收件信息'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='delivery_status',
            field=models.BooleanField(default=False, verbose_name='收货状态'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pay_status',
            field=models.BooleanField(default=False, verbose_name='支付状态'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='send_status',
            field=models.BooleanField(default=False, verbose_name='发货状态'),
        ),
        migrations.AlterField(
            model_name='tempimage',
            name='image',
            field=models.ImageField(upload_to=api.utils.changeName.changeTempName, verbose_name='暂存图片'),
        ),
        migrations.AlterField(
            model_name='tempimage',
            name='name',
            field=models.CharField(max_length=255, verbose_name='暂存图片名'),
        ),
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.CharField(max_length=128, verbose_name='token'),
        ),
        migrations.AlterField(
            model_name='token',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.CreateModel(
            name='ProgressInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='时间戳')),
                ('message', models.TextField(blank=True, null=True, verbose_name='货物运送阶段信息')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orders', verbose_name='归属订单')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1, verbose_name='物品数量')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.goodsinfo', verbose_name='物品数量')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orders', verbose_name='归属订单')),
            ],
        ),
    ]