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
from django.urls import path

from test01 import views

app_name = 'test01'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('timer/', views.timer, name='timer'),
    path('orm/', views.orm, name='orm'),
    path('orm_add/', views.orm_add, name='orm_add'),
    path('orm_delete/', views.orm_delete, name='orm_delete'),
    path('orm_modify/', views.orm_modify, name='orm_modify'),
    path('orm_search/', views.orm_search, name='orm_search'),
]
