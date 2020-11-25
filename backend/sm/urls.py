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

import test01.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('timer/', views.timer),
    path('login/', test01.views.login, name='Login'),
    re_path(r'^register/', include(('register.urls', 'register'))),
    re_path(r'^test01/', include(('test01.urls', 'test01'))),
    re_path(r'^test02/', include(('test02.urls', 'test02'))),
]
