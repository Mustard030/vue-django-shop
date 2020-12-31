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
    token = models.CharField(max_length=128)
    user = models.OneToOneField(to='auth.User', on_delete=models.CASCADE)


class Menu(models.Model):
    authName = models.CharField(max_length=10)
    path = models.CharField(max_length=128)


class ChildrenMenu(models.Model):
    authName = models.CharField(max_length=20)
    path = models.CharField(max_length=128)
    parentMenu = models.ForeignKey(to='Menu', on_delete=models.CASCADE)


class GoodsImage(models.Model):
    image = models.ImageField(upload_to=changeName)
    name = models.CharField(max_length=255)
    itemID = models.ForeignKey(to='GoodsInfo', on_delete=models.CASCADE)


class TempImage(models.Model):
    image = models.ImageField(upload_to=changeTempName)
    name = models.CharField(max_length=255)


class GoodsInfo(models.Model):
    itemClass = models.ForeignKey(to='GoodsKind', on_delete=models.CASCADE)
    merchantId = models.ForeignKey(to='Merchant', on_delete=models.CASCADE)
    itemName = models.CharField(max_length=100)
    sales = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    reserve = models.IntegerField(default=0)
    unit = models.CharField(max_length=5)
    introduce = models.TextField(blank=True, null=True)


class GoodsKind(models.Model):
    name = models.CharField(max_length=10)
    parent = models.ForeignKey(to='self', null=True, on_delete=models.CASCADE)


class Merchant(models.Model):
    admin = models.OneToOneField(to='auth.User', on_delete=models.CASCADE)
    merchantName = models.CharField(max_length=30)


class DeliveryInfo(models.Model):
    recipient = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=128, default='')
    user = models.ForeignKey(to='auth.User', on_delete=models.CASCADE)


class Orders(models.Model):
    deliveryInfo = models.ForeignKey(to='DeliveryInfo', on_delete=models.DO_NOTHING)
    pay_status = models.BooleanField(default=False)
    send_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)
    create_date = models.DateTimeField('订单创建日期', default=timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(to='Orders', on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    item = models.ForeignKey(to='GoodsInfo', on_delete=models.DO_NOTHING)

# class Area(models.Model):
#     name = models.CharField(max_length=20, verbose_name='名称')
#     # 自关联(特殊的一对多): 生成的字段名 parent_id
#     parent = models.ForeignKey(to='self', verbose_name='上级行政区划', on_delete=None)
