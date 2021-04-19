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
    path('adminLogin/', views.LoginView.as_view()),
    # 用户登录
    path('userLogin/', views.UserLoginView.as_view()),
    # 用户头像
    path('userAvatar/', views.UserAvatar.as_view()),
    # 获取左边栏菜单
    path('menus/', views.Menus.as_view()),
    # 获取每日推荐轮换图
    path('carouselPics/', views.CarouselPics.as_view()),
    # 修改用户可用状态
    path('users/<int:uid>/state/<int:state>', views.ChangeActive.as_view()),
    # 商品分类增删改查
    path('categories/', views.Categories.as_view()),
    # 根据ID获取用户信息
    path('users/<int:uid>', views.get_info_by_id),
    # 用户数据增删改查
    path('users/', views.Users.as_view()),
    # 检查用户名是否可用
    path('checkUsable/<str:check_username>', views.check_useable),
    # 检查商品类别名是否可用
    path('checkCateNameUsable/<str:check_cate_name>', views.check_cate_name_useable),
    # 商品增删改查
    path('goods/', views.Goods.as_view()),
    # 查询商品
    path('good/', views.Good.as_view()),
    # 图片上传接口
    path('itemPics/', views.ItemPics.as_view()),
    # 推荐商品列表
    path('recommendList/', views.recommendList.as_view()),
    # 获取全部商品页面信息
    path('getAllGood/', views.getAllGoodBreif),
    # 获取订单列表
    path('orders/', views.Orders.as_view()),
    # 获取订单列表(用户级)
    path('userOrder/', views.UserOrders.as_view()),
    # 搜索商品
    path('searchItem/', views.SearchItem.as_view()),
    # 搜索菜谱
    path('searchCookbook/', views.SearchCookbook.as_view()),
    # 支付接口
    path('payment/', views.Pay.as_view()),
    # 获取物流信息
    path('kuaidi/', views.Kuaidi.as_view()),
    # 用户收货地址相关
    path('delivery/', views.Delivery.as_view()),
    # 用户收货地址（用户级）
    path('userDelivery/', views.UserDelivery.as_view()),
    # 获取商家列表
    path('merchant/', views.Merchant.as_view()),
    # 菜谱相关
    path('cookbooks/', views.CookBook.as_view()),
    # 获取我的菜谱
    path('myBook/', views.MyBook.as_view()),
    # 获取未被选择的店铺管理员
    path('merchantAdmin/', views.get_merchant_admin),
    # 购物车
    path('cart/', views.Cart.as_view()),
    # 返回一个uuid
    path('uuid/', views.get_uuid),
    # 管理员欢迎页信息
    path('sold/', views.getHomePageData),
    # 测试接口
    path('test/', views.test),
    # 新增随机用户
    path('randomuser/<int:num>/', views.newRandomUser),
    # 新增随机订单
    path('randomorder/<int:num>/', views.newRandomOrder),
    # 新增随机订单（指定用户）
    path('randomorder/<int:num>/<str:user>/', views.newRandomOrderOfSb),
]
