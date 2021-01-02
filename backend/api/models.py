from django.db import models
from .utils.changeName import changeName, item_directory_path, changeTempName
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone


# Create your models here.

# 扩展user表
# class MyUserInfo(AbstractUser):
#     phone = models.CharField(max_length=11, blank=True)


# class AdminInfo(models.Model):
#     username = models.CharField(max_length=10)
#     password = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.username


class Token(models.Model):
    token = models.CharField('token', max_length=128)
    user = models.OneToOneField(verbose_name='用户', to='auth.User', on_delete=models.CASCADE)


class Menu(models.Model):
    authName = models.CharField(verbose_name='菜单名', max_length=10)
    path = models.CharField(verbose_name='路径', max_length=128)


class ChildrenMenu(models.Model):
    authName = models.CharField(verbose_name='子菜单名', max_length=20)
    path = models.CharField(verbose_name='路径', max_length=128)
    parentMenu = models.ForeignKey(verbose_name='父菜单', to='Menu', on_delete=models.CASCADE)


class GoodsImage(models.Model):
    image = models.ImageField(verbose_name='图片', upload_to=changeName)
    name = models.CharField(verbose_name='图片名', max_length=255)
    itemID = models.ForeignKey(verbose_name='归属商品', to='GoodsInfo', on_delete=models.CASCADE)


class TempImage(models.Model):
    image = models.ImageField(verbose_name='暂存图片', upload_to=changeTempName)
    name = models.CharField(verbose_name='暂存图片名', max_length=255)


class GoodsInfo(models.Model):
    itemClass = models.ForeignKey(verbose_name='商品种类', to='GoodsKind', on_delete=models.CASCADE)
    merchantId = models.ForeignKey(verbose_name='归属商家', to='Merchant', on_delete=models.CASCADE)
    itemName = models.CharField(verbose_name='商品名', max_length=100)
    sales = models.IntegerField(verbose_name='销量', default=0)
    price = models.DecimalField(verbose_name='价格', max_digits=8, decimal_places=2)
    reserve = models.IntegerField(verbose_name='库存', default=0)
    unit = models.CharField(verbose_name='单位', max_length=5)
    introduce = models.TextField(verbose_name='商品介绍', blank=True, null=True)


class GoodsKind(models.Model):
    name = models.CharField(verbose_name='商品种类名称', max_length=10)
    parent = models.ForeignKey(verbose_name='父类商品种类', to='self', null=True, on_delete=models.CASCADE)


class Merchant(models.Model):
    admin = models.OneToOneField(verbose_name='管理员', to='auth.User', on_delete=models.CASCADE)
    merchantName = models.CharField(verbose_name='商家名称', max_length=30)


class DeliveryInfo(models.Model):
    recipient = models.CharField(verbose_name='收件人姓名', max_length=10)
    phone = models.CharField(verbose_name='手机号', max_length=11)
    province = models.CharField(verbose_name='省市', max_length=30)
    address = models.CharField(verbose_name='详细地址', max_length=128, default='')
    user = models.ForeignKey(verbose_name='归属用户', to='auth.User', on_delete=models.CASCADE)


class Orders(models.Model):
    deliveryInfo = models.ForeignKey(verbose_name='收件信息', to='DeliveryInfo', on_delete=models.DO_NOTHING)
    pay_status = models.BooleanField(verbose_name='支付状态', default=False)
    send_status = models.BooleanField(verbose_name='发货状态', default=False)
    delivery_status = models.BooleanField(verbose_name='收货状态', default=False)
    create_date = models.DateTimeField(verbose_name='订单创建日期', default=timezone.now)
    mod_date = models.DateTimeField(verbose_name='最后修改日期', auto_now=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(verbose_name='归属订单', to='Orders', on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name='物品数量', default=1)
    item = models.ForeignKey(verbose_name='物品数量', to='GoodsInfo', on_delete=models.DO_NOTHING)


class ProgressInfo(models.Model):
    time = models.DateTimeField(verbose_name='时间戳', default=timezone.now)
    message = models.TextField(verbose_name='货物运送阶段信息', blank=True, null=True)
    order = models.ForeignKey(verbose_name='归属订单', to='Orders', on_delete=models.CASCADE)

# class Area(models.Model):
#     name = models.CharField(max_length=20, verbose_name='名称')
#     # 自关联(特殊的一对多): 生成的字段名 parent_id
#     parent = models.ForeignKey(to='self', verbose_name='上级行政区划', on_delete=None)
