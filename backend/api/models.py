from django.db import models
from django.contrib.auth.models import AbstractUser


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
    path = models.CharField(max_length=128, default='')


class ChildrenMenu(models.Model):
    authName = models.CharField(max_length=20)
    path = models.CharField(max_length=128, default='')
    parentMenu = models.ForeignKey(to='Menu', on_delete=models.DO_NOTHING)


class GoodsImage(models.Model):
    image = models.ImageField()


class GoodsInfo(models.Model):
    itemClass = models.ForeignKey(to='GoodsKind', on_delete=models.DO_NOTHING)
    merchantId = models.ForeignKey(to='Merchant', on_delete=models.DO_NOTHING)
    itemName = models.CharField(max_length=100)
    sales = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    reserve = models.IntegerField(default=0)
    unit = models.CharField(max_length=5)


class GoodsKind(models.Model):
    name = models.CharField(max_length=10)
    parent = models.ForeignKey(to='self', null=True, on_delete=models.CASCADE)


class Merchant(models.Model):
    admin = models.OneToOneField(to='auth.User', on_delete=models.DO_NOTHING)
    merchantName = models.CharField(max_length=30)


class DeliveryInfo(models.Model):
    recipient = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=128, default='')
    masterid = models.ForeignKey(to='auth.User', on_delete=models.DO_NOTHING)

# class Area(models.Model):
#     name = models.CharField(max_length=20, verbose_name='名称')
#     # 自关联(特殊的一对多): 生成的字段名 parent_id
#     parent = models.ForeignKey(to='self', verbose_name='上级行政区划', on_delete=None)
