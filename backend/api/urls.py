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

    path('adminLogin/', views.LoginView.as_view(), name='adminLogin'),
    path('menus/', views.menus, name='menus'),
    path('users/<int:uid>/state/<int:state>', views.change_active),
    path('categories/', views.Categories.as_view()),
    path('users/<int:uid>', views.get_info_by_id),
    path('users/', views.Users.as_view(), name='users'),
    path('checkUseable/<slug:check_username>', views.check_useable),
    path('checkCateNameUseable/<str:check_cate_name>', views.check_cate_name_useable),
]
