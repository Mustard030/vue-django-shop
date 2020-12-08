from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.urls import reverse
# from test01.models import Book
from django.contrib.auth import authenticate, login
from django.contrib import auth


# Create your views here.
def timer(requset):
    import time
    # context = dict()
    # context['timer'] = time.time()
    i = 2
    return render(requset, 'timer.html', locals())


def index(request):
    return HttpResponse(reverse("test01:index"))


def userlogin(request):
    print(reverse('Login'))
    if request.method == 'GET':
        print(request.GET)
        return render(request, 'login.html')
    else:
        print(request.POST)
        jiemoo = auth.authenticate(username='jiemoo', password='123456')
        login(request, jiemoo)
        return HttpResponse("OK " + jiemoo.username)


def orm(request):
    if request.method == 'GET':
        return render(request, 'test01/orm.html')
    else:
        return HttpResponse("OK")


def orm_add(request):
    if request.method == "POST":
        title = request.POST.get('title')
        pub_date = request.POST.get('pub_date')
        price = request.POST.get('price')
        publish = request.POST.get('publish')
        # 方法1：直接创建对象
        # book_obj = Book.objects.create(title=title, price=price, publish=publish, pub_date=pub_date)
        # 方法2：创建对象再调用对象的save()
        book_obj = Book(title=title, price=price, publish=publish, pub_date=pub_date)
        book_obj.save()
        return HttpResponse("success add")
    else:
        return HttpResponse("非法添加")


def orm_delete(request):
    if request.method == "POST":
        pass
    else:
        return HttpResponse("非法删除")


def orm_modify(request):
    if request.method == "POST":
        pass
    else:
        return HttpResponse("非法修改")


def orm_search(request):
    if request.method == "POST":
        pass
    else:
        return HttpResponse("非法查询")
