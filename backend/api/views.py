import json
from django.contrib import auth
from django.shortcuts import render
from django.http import QueryDict
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from . import models
from .utils.token import get_token_code


# Create your views here.


class LoginView(APIView):
    def post(self, request):
        # print(request.body)
        # print(request.POST)
        data = json.loads(str(request.body, encoding='utf8'))

        res = {
            'meta': {
                'message': '登陆失败',
                'code': 400
            }}
        username = data.get('username')
        password = data.get('password')
        user_obj = auth.authenticate(username=username, password=password)
        login_success = user_obj.is_superuser or user_obj.is_staff

        if login_success:
            # user_obj = models.AdminInfo.objects.get(username=data.get('username'),
            #                                         password=data.get('password'))

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
        res = {
            'data': {},
            'meta': {
                'message': '添加用户失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        username = data.get('username', '')
        password = data.get('password', '')
        mg_state = data.get('mg_state', '')
        if not username:
            return JsonResponse(res, safe=False)
        if mg_state == 3:
            user = User.objects.create_superuser(username=username, password=password)
        elif mg_state == 2:
            user = User.objects.create_superuser(username=username, password=password)
            user.is_superuser = 0
        else:
            user = User.objects.create_user(username=username, password=password)
        user.save()
        if user:
            res['meta']['message'] = '添加用户成功'
            res['meta']['code'] = 201
        return JsonResponse(res, safe=False)

    def get(self, request):
        res = {
            'data': {},
            'meta': {
                'message': '获取数据失败',
                'code': 400
            }}
        query = request.GET.get('query', '')
        pagenum = int(request.GET.get('pagenum', ''))
        pagesize = int(request.GET.get('pagesize', ''))
        head: int = (pagenum - 1) * pagesize
        tail: int = pagenum * pagesize
        total = User.objects.filter(username__icontains=query).count()
        userlist = User.objects.filter(username__icontains=query)[head:tail]

        return_list = list()
        for subuser in userlist:
            user = dict()
            user['id'] = subuser.pk
            user['username'] = subuser.username
            user['password'] = subuser.password
            role = '普通用户'
            if subuser.is_staff:
                role = '商家'
            if subuser.is_superuser:
                role = '管理员'
            user['role_name'] = role
            user['state'] = bool(subuser.is_active)

            return_list.append(user)

        res['data']['userlist'] = return_list
        res['data']['total'] = total
        # if return_list:
        res['meta']['message'] = '获取数据成功'
        res['meta']['code'] = 200

        return JsonResponse(res, safe=False)

    def delete(self, request):
        res = {
            'meta': {
                'message': '删除用户失败',
                'code': 500
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        uid = data.get('id', 0)
        user = User.objects.get(pk=uid)
        user.delete()
        if user:
            res['meta']['message'] = '删除用户成功'
            res['meta']['code'] = 200

        return JsonResponse(res, safe=False)

    def put(self, request):
        res = {
            'meta': {
                'message': '修改密码失败',
                'code': 500
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        uid = data.get('id', 0)
        password = data.get('password', '')
        if not password:
            return JsonResponse(res, safe=False)
        user = User.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        if user:
            res['meta']['message'] = '修改密码成功'
            res['meta']['code'] = 201

        return JsonResponse(res, safe=False)

    def patch(self, request):
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


def check_useable(request, check_username):
    res = {
        'meta': {
            'message': '用户名不可用',
            'code': 500
        }}
    exist = User.objects.filter(username=check_username).exists()
    if not exist:
        res['meta']['message'] = '用户名可用'
        res['meta']['code'] = 200
    return JsonResponse(res, safe=False)


def change_active(request, **kwargs):
    res = {
        'meta': {
            'message': '修改状态失败',
            'code': 500
        }}
    uid = kwargs.get('uid', 0)
    state = kwargs.get('state', None)

    changed_user = User.objects.get(pk=uid)
    if state is not None:
        changed_user.is_active = state

    changed_user.save()
    if changed_user.is_active == state:
        res['meta']['message'] = '修改状态成功'
        res['meta']['code'] = 200
    return JsonResponse(res, safe=False)


def get_info_by_id(request, uid):
    res = {
        'data': {},
        'meta': {
            'message': '获取数据失败',
            'code': 400
        }}
    user = User.objects.get(pk=uid)
    username = user.username
    if user:
        res['data']['id'] = uid
        res['data']['username'] = username
        res['meta']['message'] = '获取数据成功'
        res['meta']['code'] = 200

    return JsonResponse(res, safe=False)
