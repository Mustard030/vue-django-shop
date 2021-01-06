from django.db import models
from .utils.changeName import changeName, item_directory_path, changeTempName, changeUserName
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
import os


# Create your models here.

# 扩展user表
class MyUserInfo(AbstractUser):
    phone = models.CharField(max_length=11, blank=True, null=True)
    userImage = models.ImageField(upload_to=changeUserName, default=os.path.join('default', 'defaultUser.png'))

    class Meta:
        ordering = ['-is_active', '-is_superuser', '-is_staff']


class Token(models.Model):
    token = models.CharField('token', max_length=128)
    user = models.OneToOneField(verbose_name='用户', to='MyUserInfo', on_delete=models.CASCADE)


# 一级菜单
class Menu(models.Model):
    authName = models.CharField(verbose_name='菜单名', max_length=10)
    path = models.CharField(verbose_name='路径', max_length=128, blank=True, null=True)
    parentMenu = models.ForeignKey(verbose_name='父菜单', to='self', on_delete=models.SET_NULL, null=True, blank=True)


# 商品图片
class GoodsImage(models.Model):
    image = models.ImageField(verbose_name='图片', upload_to=changeName)
    name = models.CharField(verbose_name='图片名', max_length=255)
    itemID = models.ForeignKey(verbose_name='归属商品', to='GoodsInfo', on_delete=models.CASCADE)


# 缓存图片
class TempImage(models.Model):
    image = models.ImageField(verbose_name='暂存图片', upload_to=changeTempName)
    name = models.CharField(verbose_name='暂存图片名', max_length=255)


# 商品信息
class GoodsInfo(models.Model):
    itemClass = models.ForeignKey(verbose_name='商品种类', to='GoodsKind', on_delete=models.CASCADE)
    merchantId = models.ForeignKey(verbose_name='归属商家', to='Merchant', on_delete=models.CASCADE)
    itemName = models.CharField(verbose_name='商品名', max_length=100)
    sales = models.IntegerField(verbose_name='销量', default=0)
    price = models.DecimalField(verbose_name='价格', max_digits=8, decimal_places=2)
    reserve = models.IntegerField(verbose_name='库存', default=0)
    unit = models.CharField(verbose_name='单位', max_length=5)
    introduce = models.TextField(verbose_name='商品介绍', blank=True, null=True)


# 商品类型
class GoodsKind(models.Model):
    name = models.CharField(verbose_name='商品种类名称', max_length=10)
    parent = models.ForeignKey(verbose_name='父类商品种类', to='self', null=True, on_delete=models.CASCADE)


# 商家
class Merchant(models.Model):
    admin = models.OneToOneField(verbose_name='管理员', to='MyUserInfo', on_delete=models.CASCADE)
    merchantName = models.CharField(verbose_name='商家名称', max_length=30)


# 收货信息
class DeliveryInfo(models.Model):
    recipient = models.CharField(verbose_name='收件人姓名', max_length=10)
    phone = models.CharField(verbose_name='手机号', max_length=11)
    province = models.CharField(verbose_name='省市', max_length=30)
    address = models.CharField(verbose_name='详细地址', max_length=128, default='')
    user = models.ForeignKey(verbose_name='归属用户', to='MyUserInfo', on_delete=models.CASCADE)


# 订单
class Orders(models.Model):
    user = models.ForeignKey(verbose_name='订单归属人', to='MyUserInfo', on_delete=models.DO_NOTHING)
    deliveryInfo = models.ForeignKey(verbose_name='收件信息', to='DeliveryInfo', on_delete=models.DO_NOTHING)
    pay_status = models.BooleanField(verbose_name='支付状态', default=False)
    send_status = models.BooleanField(verbose_name='发货状态', default=False)
    delivery_status = models.BooleanField(verbose_name='收货状态', default=False)
    create_date = models.DateTimeField(verbose_name='订单创建日期', default=timezone.now)
    mod_date = models.DateTimeField(verbose_name='最后修改日期', auto_now=True)


# 订单详情
class OrderDetail(models.Model):
    order = models.ForeignKey(verbose_name='归属订单', to='Orders', on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name='物品数量', default=1)
    item = models.ForeignKey(verbose_name='物品数量', to='GoodsInfo', on_delete=models.DO_NOTHING)


# 快递信息
class ProgressInfo(models.Model):
    time = models.DateTimeField(verbose_name='时间戳', default=timezone.now)
    message = models.TextField(verbose_name='货物运送阶段信息', blank=True, null=True)
    order = models.ForeignKey(verbose_name='归属订单', to='Orders', on_delete=models.CASCADE)


# 菜谱
class CookBooks(models.Model):
    time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    title = models.CharField(verbose_name='标题', max_length=128)
    author = models.ForeignKey(verbose_name='作者', to='MyUserInfo', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='正文', blank=True, null=True)
