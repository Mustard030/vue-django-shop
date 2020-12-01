from django.db import models
# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    register_date = models.DateField()
    classes_choices = (
        (1, '普通用户'),
        (2, 'VIP用户')
    )
    classes = models.IntegerField(choices=classes_choices, default=1)

    def __str__(self):
        return self.username


class Token(models.Model):
    token = models.CharField(max_length=128)
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
