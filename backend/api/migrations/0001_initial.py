# Generated by Django 3.1.2 on 2021-01-04 18:54

import api.utils.changeName
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('userImage', models.ImageField(default='default\\defaultUser.png', upload_to=api.utils.changeName.changeUserName)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.CharField(max_length=10, verbose_name='收件人姓名')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('province', models.CharField(max_length=30, verbose_name='省市')),
                ('address', models.CharField(default='', max_length=128, verbose_name='详细地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='归属用户')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=100, verbose_name='商品名')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='价格')),
                ('reserve', models.IntegerField(default=0, verbose_name='库存')),
                ('unit', models.CharField(max_length=5, verbose_name='单位')),
                ('introduce', models.TextField(blank=True, null=True, verbose_name='商品介绍')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authName', models.CharField(max_length=10, verbose_name='菜单名')),
                ('path', models.CharField(max_length=128, verbose_name='路径')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_status', models.BooleanField(default=False, verbose_name='支付状态')),
                ('send_status', models.BooleanField(default=False, verbose_name='发货状态')),
                ('delivery_status', models.BooleanField(default=False, verbose_name='收货状态')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='订单创建日期')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
                ('deliveryInfo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.deliveryinfo', verbose_name='收件信息')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='订单归属人')),
            ],
        ),
        migrations.CreateModel(
            name='TempImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=api.utils.changeName.changeTempName, verbose_name='暂存图片')),
                ('name', models.CharField(max_length=255, verbose_name='暂存图片名')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=128, verbose_name='token')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
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
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchantName', models.CharField(max_length=30, verbose_name='商家名称')),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='管理员')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='商品种类名称')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.goodskind', verbose_name='父类商品种类')),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='itemClass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.goodskind', verbose_name='商品种类'),
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='merchantId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.merchant', verbose_name='归属商家'),
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=api.utils.changeName.changeName, verbose_name='图片')),
                ('name', models.CharField(max_length=255, verbose_name='图片名')),
                ('itemID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.goodsinfo', verbose_name='归属商品')),
            ],
        ),
        migrations.CreateModel(
            name='CookBooks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('title', models.CharField(max_length=128, verbose_name='标题')),
                ('content', models.TextField(blank=True, null=True, verbose_name='正文')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
        ),
        migrations.CreateModel(
            name='ChildrenMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authName', models.CharField(max_length=20, verbose_name='子菜单名')),
                ('path', models.CharField(max_length=128, verbose_name='路径')),
                ('parentMenu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.menu', verbose_name='父菜单')),
            ],
        ),
    ]
