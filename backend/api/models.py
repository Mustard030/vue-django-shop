from django.db import models


# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    register_date = models.DateField(auto_now=True)
    classes_choices = (
        (1, '普通用户'),
        (2, '管理员')
    )
    classes = models.IntegerField(choices=classes_choices, default=1)

    def __str__(self):
        return self.username


class Token(models.Model):
    token = models.CharField(max_length=128)
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)


class ItemInfo(models.Model):
    item_class = models.CharField(max_length=10)
    item_name = models.CharField(max_length=100)
    sales = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    reserve = models.IntegerField(default=0, max_length=3)


