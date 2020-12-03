import json
from django.contrib.auth import *
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from . import models
from .utils.token import get_token_code


# Create your views here.


class LoginView(APIView):
    def post(self, request):
        print(request.body)
        print(request.POST)
        data = json.loads(str(request.body, encoding='utf8'))

        res = {
            'meta': {
                'message': '登陆失败',
                'code': 400
            }}

        exist_user = models.AdminInfo.objects.filter(username=data.get('username'),
                                                     password=data.get('password')).exists()
        if exist_user:
            user_obj = models.AdminInfo.objects.get(username=data.get('username'),
                                                    password=data.get('password'))
            token = get_token_code(user_obj.username)
            token_obj = models.Token.objects.filter(user_id=user_obj.id).first()
            if token_obj:
                token_obj.token = token
                token_obj.save()
            else:
                models.Token.objects.create(user_id=user_obj.id, token=token)

            res.update({'data': {
                'id': user_obj.id,
                'username': user_obj.username,
                'token': token
            }
            })
            res['meta']['message'] = '登陆成功'
            res['meta']['code'] = 200

        return JsonResponse(res, safe=False)


class Users(APIView):
    def post(self, request):
        pass

    def get(self, request):
        query = request.GET.get('query', '')
        pagenum = request.GET.get('pagenum', '')
        pagesize = request.GET.get('pagesize', '')
        pass

    def delete(self, request):
        pass

    def put(self, request):
        pass


def menus(request):
    res = {
        'meta': {
            'message': '获取数据失败',
            'code': 400
        }}
    menu_list = list()
    items = models.Menu.objects.all()
    for item in items:
        parent = dict()
        children_list = list()
        parent['id'] = item.pk
        parent['path'] = item.path
        parent['authname'] = item.authName
        parent['children'] = children_list

        for ch_obj in list(item.childrenmenu_set.all()):
            children = dict()
            children['id'] = ch_obj.pk
            children['authname'] = ch_obj.authName
            children['path'] = ch_obj.path
            children_list.append(children)

        menu_list.append(parent)
    res.update({'data': menu_list})

    res['meta']['message'] = '获取数据成功'
    res['meta']['code'] = 200

    return JsonResponse(res, safe=False)


def item_manage(request):
    res = {
        'meta': {
            'message': '获取数据失败',
            'code': 400
        }}
    item_class_list = list()
    item_class = models.ItemInfo.objects.values('item_class').distinct().order_by()
    for item in item_class:
        item_class_list.append(item)
    res.update({'data': item_class_list})

    res['meta']['message'] = '获取数据成功'
    res['meta']['code'] = 200
    return JsonResponse(res, safe=False)
