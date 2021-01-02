"""sm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from api import views

app_name = 'api'

urlpatterns = [
    # 管理员登陆
    path('adminLogin/', views.LoginView.as_view(), name='adminLogin'),
    # 获取左边栏菜单
    path('menus/', views.menus, name='menus'),
    # 修改用户可用状态
    path('users/<int:uid>/state/<int:state>', views.change_active),
    # 商品分类增删改查
    path('categories/', views.Categories.as_view(), name='categories'),
    # 根据ID获取用户信息
    path('users/<int:uid>', views.get_info_by_id),
    # 用户数据增删改查
    path('users/', views.Users.as_view(), name='users'),
    # 检查用户名是否可用
    path('checkUsable/<slug:check_username>', views.check_useable),
    # 检查商品类别名是否可用
    path('checkCateNameUsable/<str:check_cate_name>', views.check_cate_name_useable),
    # 商品增删改查
    path('goods/', views.Goods.as_view(), name='goods'),
    # 图片上传接口
    path('itemPics/<int:itemid>', views.ItemPics.as_view()),
    # 临时图片接口
    path('tempImage/', views.tempImage, name="tempImage"),
    # 根据商品ID获得图片接口
    path('getImgById/', views.get_img_by_id, name="getImg"),
    # 获取订单列表
    path('orders/', views.get_orders_list, name="getOrdersList"),
    # 获取物流信息
    path('kuaidi/', views.Kuaidi.as_view()),
]
