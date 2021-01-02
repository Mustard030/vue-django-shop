import json
import os
import datetime as dt
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from rest_framework.views import APIView
from . import models
from django.conf import settings
from django.db.utils import IntegrityError
from .utils.token import get_token_code
from django.core.files import File
from django.db.models import Q


# Create your views here.


class LoginView(APIView):
    # 登陆
    def post(self, request):

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
    # 添加用户
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

    # 获取用户列表
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

    # 删除用户
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

    # 修改用户密码
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


# 获取侧边栏菜单
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


# def item_manage(request):
#     res = {
#         'meta': {
#             'message': '获取数据失败',
#             'code': 400
#         }}
#     item_class_list = list()
#     item_class = models.GoodsInfo.objects.values('itemClass').distinct().order_by()
#     for item in item_class:
#         item_class_list.append(item)
#     res.update({'data': item_class_list})

# res['meta']['message'] = '获取数据成功'
# res['meta']['code'] = 200
# return JsonResponse(res, safe=False)

# 检查用户名是否可用
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


# 检查分类名是否可用
def check_cate_name_useable(request, check_cate_name):
    res = {
        'meta': {
            'message': '分类名不可用',
            'code': 500
        }}
    exist = models.GoodsKind.objects.filter(name=check_cate_name).exists()
    if not exist:
        res['meta']['message'] = '分类名可用'
        res['meta']['code'] = 200
    return JsonResponse(res, safe=False)


# 修改用户可用状态
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


# 根据ID获取用户信息
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


# 商品图片接口
class ItemPics(APIView):
    def post(self, request, itemid):
        res = {
            'data': {},
            'meta': {
                'message': '图片上传失败',
                'code': 400
            }}

        item = models.GoodsInfo.objects.filter(pk=itemid).first()

        new_img = models.GoodsImage(
            image=request.FILES.get('file'),
            name=request.FILES.get('file').name,
            itemID=item
        )
        new_img.save()
        if new_img.image.url:
            res['data']['id'] = new_img.pk
            res['data']['url'] = new_img.image.url
            res['data']['name'] = new_img.name
            res['meta']['code'] = 200
            res['meta']['message'] = '图片上传成功'

        return JsonResponse(res, safe=False)

    def delete(self, request, itemid):
        res = {
            'data': {},
            'meta': {
                'message': '图片删除失败',
                'code': 400
            }}
        itemPic = models.GoodsImage.objects.filter(pk=itemid).first()
        itemPicPK = itemPic.pk
        picurl = itemPic.image.url
        deleteNum, deletePic = itemPic.delete()
        if deleteNum > 0:
            base = str(settings.BASE_DIR).replace('\\', '/')
            picabsurl = base + picurl
            # print(picabsurl)
            os.remove(picabsurl)
            res['data']['itemPicID'] = itemPicPK
            res['meta']['code'] = 200
            res['meta']['message'] = '图片删除成功'

        return JsonResponse(res, safe=False)


def tempImage(request):
    res = {
        'data': {},
        'meta': {
            'message': '图片上传失败',
            'code': 400
        }}
    temp_img = models.TempImage(
        image=request.FILES.get('file'),
        name=request.FILES.get('file').name,
    )

    temp_img.save()
    if temp_img.image.url:
        res['data']['id'] = temp_img.pk
        res['data']['url'] = temp_img.image.url
        res['data']['name'] = temp_img.name
        res['meta']['code'] = 200
        res['meta']['message'] = '图片上传成功'

    return JsonResponse(res, safe=False)


def get_img_by_id(request):
    pass


# 商品分类
class Categories(APIView):
    # 根据级别获取商品分类
    def get(self, request):
        res = {
            'meta': {
                'message': '获取数据失败',
                'code': 400
            }}
        # 获取1、2级商品类别
        if request.GET.get('type') == '2':
            data_list = list()
            categories_list = models.GoodsKind.objects.filter(parent=None)
            for klass in categories_list:
                klass_dict = dict()
                klass_children = list()

                klass_dict['cat_id'] = klass.pk
                klass_dict['cat_name'] = klass.name
                klass_dict['cat_level'] = 0
                children_list = models.GoodsKind.objects.filter(parent=klass.pk)
                for children in children_list:
                    children_dict = dict()
                    children_dict['cat_id'] = children.pk
                    children_dict['cat_name'] = children.name
                    children_dict['cat_level'] = 1

                    klass_children.append(children_dict)

                klass_dict['children'] = klass_children
                data_list.append(klass_dict)
            if data_list:
                res['data'] = data_list
                res['meta']['message'] = '获取数据成功'
                res['meta']['code'] = 200

        # 仅获取父级商品类别
        elif request.GET.get('type') == '1':
            data_list = list()
            categories_list = models.GoodsKind.objects.filter(parent=None)
            for klass in categories_list:
                klass_dict = dict()
                klass_dict['cat_id'] = klass.pk
                klass_dict['cat_name'] = klass.name
                klass_dict['cat_level'] = 0
                data_list.append(klass_dict)
            if data_list:
                res['data'] = data_list
                res['meta']['message'] = '获取数据成功'
                res['meta']['code'] = 200

        return JsonResponse(res, safe=False)

    # 添加商品分类
    def put(self, request):
        res = {
            'meta': {
                'message': '获取数据失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        cat_name = data.get('cat_name')
        parent_cate_id = data.get('parentCateId', None)
        if models.GoodsKind.objects.filter(name=cat_name).exists():
            res['meta']['code'] = 500
            res['meta']['message'] = '数据已存在'
            return JsonResponse(res, safe=False)

        # 获得父级分类
        parent_cate = models.GoodsKind.objects.get(pk=parent_cate_id) if parent_cate_id else None

        try:
            new_cate = models.GoodsKind(name=cat_name, parent=parent_cate)
            new_cate.save()
            cat_level = 1 if parent_cate_id else 0
            res['data'] = {
                'cat_id': new_cate.pk,
                'cat_name': new_cate.name,
                'cat_level': cat_level
            }
            res['meta']['code'] = 200
            res['meta']['message'] = '数据添加成功'
        except Exception as e:
            print(e)

        return JsonResponse(res, safe=False)

    # 修改商品分类名称
    def post(self, request):
        res = {
            'meta': {
                'message': '修改分类名失败',
                'code': 500
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        cat_id = data.get('cat_id')
        cat_name = data.get('cat_name')
        change_kind = models.GoodsKind.objects.get(pk=cat_id)
        if change_kind:
            change_kind.name = cat_name
            change_kind.save()
            res['meta']['message'] = '修改分类名成功'
            res['meta']['code'] = 200
        return JsonResponse(res, safe=False)

    # 删除商品分类(级联删除)
    def delete(self, request):
        res = {
            'meta': {
                'message': '删除分类失败',
                'code': 500
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        cat_id = data.get('id', None)
        if cat_id:
            delete_kind = models.GoodsKind.objects.get(pk=cat_id)
            delete_kind.delete()
            if delete_kind:
                res['meta']['message'] = '删除分类成功'
                res['meta']['code'] = 200

        return JsonResponse(res, safe=False)


# 商品列表
class Goods(APIView):

    # 获取商品列表
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
        categoryId = int(request.GET.get('categoryId', 0))
        head: int = (pagenum - 1) * pagesize
        tail: int = pagenum * pagesize
        if categoryId:
            total = models.GoodsInfo.objects.filter(itemName__icontains=query, itemClass=categoryId).count()
            goodslist = models.GoodsInfo.objects.filter(itemName__icontains=query, itemClass=categoryId)[head:tail]
        else:
            total = models.GoodsInfo.objects.filter(itemName__icontains=query).count()
            goodslist = models.GoodsInfo.objects.filter(itemName__icontains=query)[head:tail]

        return_list = list()
        for subitem in goodslist:
            item = dict()
            item['id'] = subitem.pk
            item['itemName'] = subitem.itemName
            item['sales'] = subitem.sales
            item['price'] = subitem.price
            item['reserve'] = subitem.reserve
            item['itemClass'] = subitem.itemClass.name
            item['merchantName'] = subitem.merchantId.merchantName
            item['unit'] = subitem.unit

            return_list.append(item)

        res['data']['goodslist'] = return_list
        res['data']['total'] = total
        # if return_list:
        res['meta']['message'] = '获取数据成功'
        res['meta']['code'] = 200

        return JsonResponse(res, safe=False)

    # 添加商品
    def post(self, request):
        res = {
            'data': {},
            'meta': {
                'message': '添加商品失败',
                'code': 500
            }}
        data = json.loads(str(request.body, encoding='utf8'))

        itemName = data.get('itemName')
        price = data.get('price')
        reserve = data.get('reserve')
        itemClasspk = data.get('itemClass')
        itemClass = models.GoodsKind.objects.filter(pk=itemClasspk).first()
        merchant_pk = data.get('merchant', 1)
        merchant = models.Merchant.objects.filter(pk=merchant_pk).first()
        unit = data.get('unit')
        introduce = data.get('introduce', None)
        pics = data.get('pics', list())
        # 添加商品条目
        new_item = models.GoodsInfo(itemName=itemName,
                                    price=price,
                                    reserve=reserve,
                                    itemClass=itemClass,
                                    unit=unit,
                                    merchantId=merchant,
                                    introduce=introduce)
        new_item.save()
        for pic in pics:
            tempPic = models.TempImage.objects.filter(pk=pic).first()
            pic_name = tempPic.name
            with open(tempPic.image.path, 'rb') as f:
                image = File(f)
                new_pic = models.GoodsImage(image=image, name=pic_name, itemID=new_item)
                new_pic.save()
            os.remove(tempPic.image.path)
            tempPic.delete()

        if new_item:
            res['data']['newItemID'] = new_item.pk
            res['meta']['code'] = 200
            res['meta']['message'] = '添加商品成功'
        return JsonResponse(res, safe=False)

    # 根据ID删除商品信息
    def delete(self, request):
        res = {
            'meta': {
                'message': '删除商品失败',
                'code': 500
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        uid = data.get('id', 0)
        item = models.GoodsInfo.objects.get(pk=uid)
        if item:
            item.delete()
            res['meta']['message'] = '删除商品成功'
            res['meta']['code'] = 200

        return JsonResponse(res, safe=False)


def get_orders_list(request):
    res = {
        'data': {},
        'meta': {
            'message': '获取数据失败',
            'code': 400
        }}
    data = request.GET
    query = data.get('query')
    print(query)
    try:
        start, end = str(query).split(',')
    except ValueError:
        start = datetime(dt.MINYEAR, 1, 1, 0, 0, 0, 0)
        end = datetime(dt.MAXYEAR, 1, 1, 0, 0, 0, 0)
    else:
        start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

    pagenum = int(data.get('pagenum', ''))
    pagesize = int(data.get('pageSize', ''))
    head: int = (pagenum - 1) * pagesize
    tail: int = pagenum * pagesize
    total = models.Orders.objects.filter(create_date__range=(start, end)).count()
    order_list = models.Orders.objects.filter(create_date__range=(start, end))[head:tail]

    return_list = list()
    for order in order_list:
        order_dict = dict()
        order_dict['order_number'] = order.pk
        order_dict['pay_status'] = order.pay_status
        order_dict['send_status'] = order.send_status
        order_dict['delivery_status'] = order.delivery_status
        create_time = str(order.create_date).replace('T', ' ')
        order_dict['create_time'] = create_time
        total_prices = 1
        order_dict['order_price'] = total_prices

        return_list.append(order_dict)

    res['data'].update({'orderList': return_list})
    res['data'].update({'total': total})
    res['meta']['code'] = 200
    res['meta']['message'] = '获取数据成功'

    return JsonResponse(res, safe=False)


# 快递接口
class Kuaidi(APIView):
    # 根据订单编号获取物流信息
    def get(self, request):
        res = {
            'meta': {
                'message': '获取快递信息失败',
                'code': 400
            }}
        kuaidi_id = request.GET.get('id')
        order_obj = models.Orders.objects.filter(pk=kuaidi_id).first()
        kuaidi_list = models.ProgressInfo.objects.filter(order=order_obj).order_by('time')
        return_list = list()
        for k in kuaidi_list:
            k_dict = dict()
            k_dict['id'] = k.pk
            k_dict['time'] = str(k.time).replace('T', ' ')
            k_dict['message'] = k.message
            return_list.append(k_dict)
        res.update({'data': return_list})
        res['meta']['code'] = 200
        res['meta']['message'] = '获取快递信息成功'

        return JsonResponse(res, safe=False)

    # 根据订单编号更新物流信息
    def put(self, request):
        res = {
            'data': {},
            'meta': {
                'message': '获取快递信息失败',
                'code': 400
            }}
        return JsonResponse(res, safe=False)
