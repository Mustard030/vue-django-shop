from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# 扩展user表
# class MyUserInfo(AbstractUser):
#     phone = models.CharField(max_length=11, blank=True)


class AdminInfo(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Token(models.Model):
    token = models.CharField(max_length=128)
    user = models.OneToOneField(to='AdminInfo', on_delete=models.CASCADE)


class Menu(models.Model):
    authName = models.CharField(max_length=10)
    path = models.CharField(max_length=128, default='')


class ChildrenMenu(models.Model):
    authName = models.CharField(max_length=20)
    path = models.CharField(max_length=128, default='')
    parentMenu = models.ForeignKey(to='Menu', on_delete=models.PROTECT)


class ItemInfo(models.Model):
    item_class = models.CharField(max_length=10)
    item_name = models.CharField(max_length=100)
    sales = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    reserve = models.IntegerField(default=0)


class UserInfo(models.Model):
    address = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)
    recipient = models.CharField(max_length=10)


class DeliveryInfo(models.Model):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    masterid = models.ForeignKey(to='auth.User', on_delete=models.CASCADE)
