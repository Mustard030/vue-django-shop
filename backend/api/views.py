import json
import os
import datetime as dt
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.models import Group
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from rest_framework.views import APIView
from . import models
from django.conf import settings
from django.db.utils import IntegrityError
from .utils.token import get_token_code
from django.core.files import File
from django.db.models import Q
from .utils.decorator import need_login


# Create your views here.


class LoginView(APIView):
    # 管理员登陆
    def post(self, request):
        res = {
            'meta': {
                'message': '登陆失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        username = data.get('username')
        password = data.get('password')
        # user = auth.get_user_model()
        user_obj = auth.authenticate(username=username, password=password)
        login_success = user_obj.is_superuser  # or user_obj.is_staff

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
                'token': token,
                'avatar': user_obj.userImage.url,
                'is_superuser': True if user_obj.is_superuser else False
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
        User = auth.get_user_model()
        username = data.get('username', '')
        password = data.get('password', '')
        phone = data.get('phone', '')
        email = data.get('email', '')
        mg_state = data.get('mg_state', 1)
        if not username:
            return JsonResponse(res, safe=False)
        if mg_state == 3:
            user = User.objects.create_superuser(username=username, password=password, phone=phone, email=email)
        elif mg_state == 2:
            user = User.objects.create_superuser(username=username, password=password, phone=phone, email=email)
            user.is_superuser = 0
        else:
            user = User.objects.create_user(username=username, password=password, phone=phone, email=email)
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

        User = auth.get_user_model()
        search_dict = dict()
        args = tuple()

        query = request.GET.get('query')
        if query:
            search_dict['username__icontains'] = query
        is_staff = request.GET.get('is_staff')
        if is_staff == 'true':
            search_dict['is_staff'] = True
            search_dict['is_superuser'] = False

        is_superuser = request.GET.get('is_superuser')
        if is_superuser == 'true':
            search_dict['is_superuser'] = True

        pagenum = int(request.GET.get('pagenum', ''))
        pagesize = int(request.GET.get('pagesize', ''))
        head: int = (pagenum - 1) * pagesize
        tail: int = pagenum * pagesize
        total = User.objects.filter(*args, **search_dict).count()
        userlist = User.objects.filter(*args, **search_dict)[head:tail]

        return_list = list()
        for subuser in userlist:
            user = dict()
            user['id'] = subuser.pk
            user['username'] = subuser.username
            user['password'] = subuser.password
            user['phone'] = subuser.phone
            user['email'] = subuser.email
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
        User = auth.get_user_model()
        uid = data.get('id', 0)
        user = User.objects.get(pk=uid)
        user.delete()
        if user:
            res['meta']['message'] = '删除用户成功'
            res['meta']['code'] = 200

        return JsonResponse(res, safe=False)

    # 修改用户信息
    def put(self, request):
        res = {
            'meta': {
                'message': '修改信息失败',
                'code': 500
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        User = auth.get_user_model()
        uid = data.get('id', 0)
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        email = data.get('email')
        user = User.objects.get(pk=uid)
        if username:
            if models.MyUserInfo.objects.filter(username=username).exists():
                res['meta']['code'] = 500
                res['meta']['message'] = '用户名已被使用'
                return JsonResponse(res, safe=False)
            else:
                user.username = username
        if password:
            user.set_password(password)
        if phone:
            user.phone = phone
        if email:
            user.email = email
        user.save()
        if user:
            res['meta']['message'] = '修改信息成功'
            res['meta']['code'] = 201

        return JsonResponse(res, safe=False)

    # 修改用户角色
    def patch(self, request):
        res = {
            'meta': {
                'message': '修改角色失败',
                'code': 500
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        User = auth.get_user_model()
        uid = int(data.get('id', 0))
        role = data.get('role', 0)

        if uid and role:
            user = User.objects.get(pk=uid)
            if role == 1:
                if models.Merchant.objects.filter(admin=uid).exists():
                    res['meta']['code'] = 500
                    res['meta']['message'] = '请先删除此用户下绑定的商铺'
                    return JsonResponse(res, safe=False)
                else:
                    user.is_staff, user.is_superuser = 0, 0
            elif role == 2:
                user.is_staff, user.is_superuser = 1, 0
            elif role == 3:
                user.is_staff, user.is_superuser = 1, 1
            user.save()

            res['meta']['code'] = 200
            res['meta']['message'] = '修改角色成功'

        return JsonResponse(res, safe=False)


# 获取侧边栏菜单
class Menus(APIView):
    def get(self, request):
        res = {
            'meta': {
                'message': '获取数据失败',
                'code': 400
            }}
        menu_list = list()
        items = models.Menu.objects.filter(parentMenu__isnull=True)
        for item in items:
            parent = dict()
            children_list = list()
            parent['id'] = item.pk
            parent['path'] = item.path
            parent['authname'] = item.authName
            parent['children'] = children_list

            for ch_obj in list(item.menu_set.all()):
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
    exist = models.MyUserInfo.objects.filter(username=check_username).exists()
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
class ChangeActive(APIView):
    def put(self, request, **kwargs):
        res = {
            'meta': {
                'message': '修改状态失败',
                'code': 500
            }}
        uid = kwargs.get('uid', 0)
        state = kwargs.get('state', None)
        User = auth.get_user_model()
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
    User = auth.get_user_model()
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
    def post(self, request):
        res = {
            'data': {},
            'meta': {
                'message': '图片上传失败',
                'code': 400
            }}

        new_img = models.GoodsImage(
            image=request.FILES.get('file'),
            name=request.FILES.get('file').name,
        )
        new_img.save()
        if new_img.image.url:
            res['data']['id'] = new_img.pk
            res['data']['url'] = settings.RUNNING_HOST + new_img.image.url
            res['data']['name'] = new_img.name
            res['meta']['code'] = 200
            res['meta']['message'] = '图片上传成功'

        return JsonResponse(res, safe=False)

    def delete(self, request):
        res = {
            'data': {},
            'meta': {
                'message': '图片删除失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        # print(data)
        del_pk = int(data.get('id'))
        itemPic = models.GoodsImage.objects.filter(pk=del_pk).first()

        res['data']['itemPicID'] = int(itemPic.pk)
        res['meta']['code'] = 200
        res['meta']['message'] = '图片删除成功'

        os.remove(itemPic.image.path)
        itemPic.delete()
        return JsonResponse(res, safe=False)


# 暂存图片接口
class TempImage(APIView):
    def post(self, request):
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
            res['data']['url'] = 'http://localhost:80' + temp_img.image.url
            res['data']['name'] = temp_img.name
            res['meta']['code'] = 200
            res['meta']['message'] = '图片上传成功'

        return JsonResponse(res, safe=False)

    def delete(self, request):
        res = {
            'meta': {
                'message': '图片删除失败',
                'code': 400
            }}
        # print(request.body)
        data = json.loads(str(request.body, encoding='utf8'))
        pk = data.get('id')
        del_pic = models.TempImage.objects.filter(pk=pk).first()
        if del_pic:
            os.remove(del_pic.image.path)
            del_pic.delete()
            res['meta']['code'] = 200
            res['meta']['message'] = '删除图片成功'
        return JsonResponse(res, safe=False)


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
        item = request.GET.get('id')

        if not item:
            query = request.GET.get('query', '')
            pagenum = int(request.GET.get('pagenum', 0))
            pagesize = int(request.GET.get('pagesize', 0))
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
                item['introduce'] = subitem.introduce

                return_list.append(item)

            res['data']['goodslist'] = return_list
            res['data']['total'] = total
            # if return_list:
            res['meta']['message'] = '获取数据成功'
            res['meta']['code'] = 200
        elif item:
            item_obj = models.GoodsInfo.objects.filter(pk=item).first()
            if item_obj:
                pics_list = item_obj.goodsimage_set.all()
                pics = list()
                for pic in pics_list:
                    pic_obj = dict()
                    pic_obj['id'] = pic.pk
                    pic_obj['url'] = settings.RUNNING_HOST + pic.image.url
                    pics.append(pic_obj)

                res['data'].update({
                    'id': item_obj.pk,
                    'name': item_obj.itemName,
                    'sales': item_obj.sales,
                    'price': item_obj.price,
                    'reserve': item_obj.reserve,
                    'unit': item_obj.unit,
                    'introduce': item_obj.introduce,
                    'merchant': item_obj.merchantId.admin.pk,
                    'itemClass': [item_obj.itemClass.parent.pk, item_obj.itemClass.pk],
                    'pics': pics
                })
                res['meta']['code'] = 200
                res['meta']['message'] = '获取数据成功'

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
        itemClasspk = data.get('itemClass')[-1]
        itemClass = models.GoodsKind.objects.filter(pk=itemClasspk).first()
        merchant_pk = int(data.get('merchant'))
        merchant = models.Merchant.objects.filter(admin=merchant_pk).first()
        unit = data.get('unit')
        introduce = data.get('introduce')
        introduce = '此商品未填写介绍' if not introduce else introduce
        print(introduce)
        pics = data.get('pics', [])
        # 添加商品条目
        new_item = models.GoodsInfo(itemName=itemName,
                                    price=price,
                                    reserve=reserve,
                                    itemClass=itemClass,
                                    unit=unit,
                                    merchantId=merchant,
                                    introduce=introduce)
        new_item.save()
        if pics:
            for pic in pics:
                pic_obj = models.GoodsImage.objects.filter(pk=pic['id']).first()
                pic_obj.itemID = new_item
                pic_obj.save()

        if new_item:
            res['data']['newItemID'] = new_item.pk
            res['meta']['code'] = 200
            res['meta']['message'] = '添加商品成功'
        return JsonResponse(res, safe=False)

    # 根据ID删除商品
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

    # 修改商品信息
    def put(self, request):
        res = {
            'meta': {
                'message': '修改商品失败',
                'code': 500
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        # print(data)
        # {'id': '2', 'itemName': '新鲜白菜 无农药残留', 'price': '3.00', 'reserve': 100, 'itemClass': [3, 31], 'unit': '斤',
        #  'merchant': 8, 'introduce': '<p>新鲜大白菜啊！快来买啊！！真的很好吃</p>', 'pics': [
        #     {'id': 44, 'url': 'http://localhost:80/media/itemPics/4b9df4d4a2dd8ab69a61db029b6bf480.jpg',
        #      'uid': 1610373347237, 'status': 'success'}]}
        pk = int(data.get('id'))
        itemName = data.get('itemName')
        price = data.get('price')
        reserve = data.get('reserve')
        itemClass = data.get('itemClass')[-1]
        unit = data.get('unit')
        merchantID = data.get('merchant')
        introduce = data.get('introduce')
        pics = data.get('pics')
        item_obj = models.GoodsInfo.objects.filter(pk=pk).first()
        if item_obj:
            item_obj.itemName = itemName
            item_obj.price = price
            item_obj.reserve = reserve
            item_obj.itemClass = models.GoodsKind.objects.filter(pk=itemClass).first()
            item_obj.unit = unit
            item_obj.introduce = introduce
            item_obj.unmerchant = models.Merchant.objects.filter(admin=merchantID).first()

            if pics:
                for pic in pics:
                    pic_obj = models.GoodsImage.objects.filter(pk=pic['id']).first()
                    pic_obj.itemID = item_obj
                    pic_obj.save()
            item_obj.save()

            res['meta']['code'] = 200
            res['meta']['message'] = '修改商品成功'

        return JsonResponse(res, safe=False)


# 订单相关接口
class Orders(APIView):
    # 获取订单列表
    def get(self, request):
        res = {
            'data': {},
            'meta': {
                'message': '获取数据失败',
                'code': 400
            }}
        data = request.GET
        query = data.get('query')
        # print(query)
        if query == '':
            start = datetime(dt.MINYEAR, 1, 1, 0, 0, 0, 0)
            end = datetime(dt.MAXYEAR, 1, 1, 0, 0, 0, 0)
        else:
            start, end = str(query).split(',')
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
            detail_list = list()
            order_dict['order_number'] = order.pk
            order_dict['pay_status'] = order.pay_status
            order_dict['send_status'] = order.send_status
            order_dict['delivery_status'] = order.delivery_status
            create_time = str(order.create_date).replace('T', ' ')
            order_dict['create_time'] = create_time
            total_prices = 0
            for item_obj in order.orderdetail_set.all():
                item_dict = dict()
                item_dict['itemID'] = item_obj.item.pk
                item_dict['itemName'] = item_obj.item.itemName
                item_dict['price'] = item_obj.item.price
                item_dict['number'] = item_obj.number
                detail_list.append(item_dict)
                total_prices += item_obj.item.price * item_obj.number

            order_dict['detailList'] = detail_list
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


# 用户收货信息
class Delivery(APIView):
    # 获取地址列表
    def get(self, request):
        res = {
            'meta': {
                'message': '获取地址信息失败',
                'code': 400
            }}

        search_dict = dict()
        args = tuple()
        query = request.GET.get('query')
        select = request.GET.get('select')
        if select == 'recipient':
            args = (Q(recipient__icontains=query))
            # search_dict['recipient__icontains'] = query
        elif select == 'phone':
            args = (Q(phone__icontains=query))
            # search_dict['phone__icontains'] = query
        elif select == 'username':
            args = (Q(user__username__icontains=query))
            # search_dict['user__username__icontains'] = query
        elif select == 'address':
            args = (Q(address__icontains=query))
            # search_dict['address__icontains'] = query
        else:
            args = (Q(recipient__icontains=query) |
                    Q(phone__icontains=query) |
                    Q(address__icontains=query) |
                    Q(user__username__icontains=query))
        province = request.GET.getlist('province[]')

        if province:
            province = '/'.join(province)
            search_dict['province'] = province

        pagenum = int(request.GET.get('pagenum', ''))
        pagesize = int(request.GET.get('pagesize', ''))
        head: int = (pagenum - 1) * pagesize
        tail: int = pagenum * pagesize
        total = models.DeliveryInfo.objects.filter(args, **search_dict).count()
        dataList = models.DeliveryInfo.objects.filter(args, **search_dict)[head:tail]
        deliveryList = list()
        for data in dataList:
            data_dict = dict()
            data_dict['id'] = data.pk
            data_dict['recipient'] = data.recipient
            data_dict['phone'] = data.phone
            data_dict['province'] = data.province
            data_dict['address'] = data.address
            data_dict['user'] = data.user.username
            data_dict['userID'] = data.user.pk
            deliveryList.append(data_dict)

        res.update({'data': {}})
        res['data'].update({'deliveryList': deliveryList})
        res['data'].update({'total': total})
        res['meta']['code'] = 200
        res['meta']['message'] = '获取数据成功'
        return JsonResponse(res, safe=False)

    # 添加地址信息
    def post(self, request):
        res = {
            'meta': {
                'message': '添加地址信息失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))

        recipient = data.get('recipient')
        phone = data.get('phone')
        province = '/'.join(data.get('province'))
        address = data.get('address')
        user = models.MyUserInfo.objects.get(pk=data.get('user'))

        new_delivery = models.DeliveryInfo.objects.create(recipient=recipient,
                                                          phone=phone,
                                                          province=province,
                                                          address=address,
                                                          user=user)
        if new_delivery:
            res['meta']['message'] = '添加地址信息成功'
            res['meta']['code'] = 200

        return JsonResponse(res, safe=False)

    # 修改地址信息
    def put(self, request):
        res = {
            'meta': {
                'message': '修改地址信息失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        uid = data.get('id')
        delivery_obj = models.DeliveryInfo.objects.get(pk=uid)
        recipient = data.get('recipient')
        phone = data.get('phone')
        province = '/'.join(data.get('province'))
        address = data.get('address')
        user = models.MyUserInfo.objects.get(pk=data.get('user'))
        if delivery_obj:
            delivery_obj.recipient = recipient
            delivery_obj.phone = phone
            delivery_obj.province = province
            delivery_obj.address = address
            delivery_obj.user = user
            delivery_obj.save()
            res['meta']['message'] = '修改地址信息成功'
            res['meta']['code'] = 200

        return JsonResponse(res, safe=False)

    # 删除地址信息
    def delete(self, request):
        res = {
            'meta': {
                'message': '删除地址信息失败',
                'code': 400
            }}

        data = json.loads(str(request.body, encoding='utf8'))
        uid = data.get('id')
        item = models.DeliveryInfo.objects.get(pk=uid)
        if item:
            item.delete()
            res['meta']['message'] = '删除地址成功'
            res['meta']['code'] = 200
        return JsonResponse(res, safe=False)


# 商家相关
class Merchant(APIView):
    @staticmethod
    def get_merchant_list(merchantID, *page):
        if merchantID:
            merchant = dict()
            merchant_obj = models.Merchant.objects.filter(pk=merchantID).first()
            if merchant_obj:
                merchant['id'] = merchant_obj.pk
                merchant['name'] = merchant_obj.merchantName
                merchant['admin'] = merchant_obj.admin.pk
                merchant['introduce'] = merchant_obj.introduce
                success = True
                total = 1
            else:
                success = False
                total = 0
        elif not merchantID:
            query, head, tail = page
            merchant = list()
            merchant_list = models.Merchant.objects.filter(merchantName__icontains=query)[head:tail]
            total = models.Merchant.objects.filter(merchantName__icontains=query).count()
            for m in merchant_list:
                merchant_obj = dict()
                merchant_obj['id'] = m.pk
                merchant_obj['name'] = m.merchantName
                merchant_obj['admin'] = m.admin.pk
                merchant_obj['admin_name'] = m.admin.username
                merchant_obj['introduce'] = m.introduce
                merchant.append(merchant_obj)

            success = True if merchant else False

        else:
            success = False
            merchant = None
            total = 0

        return success, merchant, total

    def get(self, request):
        res = {
            'meta': {
                'message': '获取商铺失败',
                'code': 400
            }}
        query = request.GET.get('query', '')
        pagenum = int(request.GET.get('pagenum', 0))
        pagesize = int(request.GET.get('pagesize', 0))
        head: int = (pagenum - 1) * pagesize
        tail: int = pagenum * pagesize
        merchantID = int(request.GET.get('id', 0))
        success, merchant, total = self.get_merchant_list(merchantID, query, head, tail)
        if success:
            res.update({'data': {}})
            res['data'].update({'merchant': merchant})
            res['data'].update({'total': total})
            res['meta']['message'] = '获取商铺成功'
            res['meta']['code'] = 200

        return JsonResponse(res, safe=False)

    def post(self, request):
        res = {
            'meta': {
                'message': '新增商家信息失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        name = data.get('name')
        introduce = data.get('introduce')
        admin = models.MyUserInfo.objects.get(pk=int(data.get('admin')))
        new_merchant = models.Merchant.objects.create(merchantName=name, admin=admin, introduce=introduce)
        if new_merchant:
            res.update({'data': {}})
            res['data'].update({
                'id': new_merchant.pk,
                'name': new_merchant.merchantName,
                'admin': new_merchant.admin.pk,
                'introduce': new_merchant.introduce
            })
            res['meta']['code'] = 200
            res['meta']['message'] = '新增商铺成功'
        return JsonResponse(res, safe=False)

    def put(self, request):
        res = {
            'meta': {
                'message': '更改商家信息失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        uid = data.get('id')
        name = data.get('name')
        adminID = data.get('admin')
        introduce = data.get('introduce')
        merchant_obj = models.Merchant.objects.filter(pk=uid).first()
        if name:
            merchant_obj.name = name
        if adminID:
            merchant_obj.admin = models.MyUserInfo.objects.filter(pk=adminID).first()
        if introduce:
            merchant_obj.introduce = introduce
        merchant_obj.save()
        if merchant_obj:
            res['meta']['code'] = 200
            res['meta']['message'] = '更改商家信息成功'

        return JsonResponse(res, safe=False)

    def delete(self, request):
        res = {
            'meta': {
                'message': '删除商铺失败',
                'code': 400
            }}

        data = json.loads(str(request.body, encoding='utf8'))
        uid = data.get('id')
        item = models.Merchant.objects.get(pk=uid)
        if item:
            item.delete()
            res['meta']['message'] = '删除商铺成功'
            res['meta']['code'] = 200
        return JsonResponse(res, safe=False)


# 菜谱相关
class CookBook(APIView):
    @staticmethod
    def get_cookbook_list(query, head, tail):
        cookbook_list = list()
        cookbook_list_obj = models.CookBooks.objects.filter(title__icontains=query)[head:tail]
        total = models.CookBooks.objects.filter(title__icontains=query).count()
        for book in cookbook_list_obj:
            book_obj = dict()
            book_obj['id'] = book.pk
            book_obj['author'] = book.author.username
            book_obj['authorID'] = book.author.pk
            book_obj['title'] = book.title
            book_obj['content'] = book.content
            book_obj['create_time'] = str(book.create_time).replace('T', ' ')
            book_obj['modify_time'] = str(book.modify_time).replace('T', ' ')
            cookbook_list.append(book_obj)

        success = True

        return success, cookbook_list, total

    @staticmethod
    def get_one_cookbook(essayID):
        essay = dict()
        essay_obj = models.CookBooks.objects.filter(pk=essayID).first()
        if essay_obj:
            essay['id'] = essay_obj.pk
            essay['author'] = essay_obj.author.username
            essay['authorID'] = essay_obj.author.pk
            essay['title'] = essay_obj.title
            essay['content'] = essay_obj.content
            essay['create_time'] = str(essay_obj.create_time).replace('T', ' ')
            essay['modify_time'] = str(essay_obj.modify_time).replace('T', ' ')
            success = True
        else:
            success = False
        return success, essay

    # 获取菜谱列表或特定文章
    def get(self, request):
        res = {
            'meta': {
                'message': '获取菜谱失败',
                'code': 400
            }}
        query = request.GET.get('query', '')
        pagenum = int(request.GET.get('pagenum', 0))
        pagesize = int(request.GET.get('pagesize', 0))
        head: int = (pagenum - 1) * pagesize
        tail: int = pagenum * pagesize
        essayID = int(request.GET.get('id', 0))

        if not essayID:
            success, essay_list, total = self.get_cookbook_list(query, head, tail)
            if success:
                res.update({'data': {}})
                res['data']['cookbookList'] = essay_list
                res['data']['total'] = total
                res['meta']['code'] = 200
                res['meta']['message'] = '获取菜谱成功'

        elif essayID:
            success, essay = self.get_one_cookbook(essayID)
            if success:
                res.update({'data': {}})
                res['data'].update({'cookbook': essay})
                res['meta']['code'] = 200
                res['meta']['message'] = '获取菜谱成功'

        return JsonResponse(res, safe=False)

    # 添加菜谱
    def post(self, request):
        res = {
            'meta': {
                'message': '添加菜谱失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        title = data.get('title', '')
        author = data.get('author', 0)
        content = data.get('content', '')
        if title and author and content:
            new_book = models.CookBooks.objects.create(title=title,
                                                       author=models.MyUserInfo.objects.filter(pk=author).first(),
                                                       content=content)
            if new_book:
                res['meta']['code'] = 200
                res['meta']['message'] = '添加菜谱成功'

        return JsonResponse(res, safe=False)

    # 修改菜谱
    def put(self, request):
        res = {
            'meta': {
                'message': '修改菜谱失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        essayID = data.get('essayID', 0)
        title = data.get('title', '')
        author = data.get('author', 0)
        content = data.get('content', '')
        essay = models.CookBooks.objects.filter(pk=essayID).first()
        if title:
            essay.title = title
        if author:
            essay.author = models.MyUserInfo.objects.filter(pk=author).first()
        if content:
            essay.content = content
        if essay:
            res['meta']['code'] = 200
            res['meta']['message'] = '修改菜谱成功'
            essay.save()

        return JsonResponse(res, safe=False)

    # 删除菜谱
    def delete(self, request):
        res = {
            'meta': {
                'message': '删除菜谱失败',
                'code': 400
            }}
        data = json.loads(str(request.body, encoding='utf8'))
        uid = data.get('id')
        item = models.CookBooks.objects.get(pk=uid)
        if item:
            item.delete()
            res['meta']['message'] = '删除文章成功'
            res['meta']['code'] = 200
        return JsonResponse(res, safe=False)


def get_merchant_admin(request):
    res = {
        'meta': {
            'message': '获取未指派的商铺管理员列表失败',
            'code': 400
        }}
    user_list = models.MyUserInfo.objects.filter(is_staff=True, is_superuser=False) \
        .exclude(pk__in=models.Merchant.objects.all().values_list('admin'))
    admin_list = list()
    if user_list:
        for user in user_list:
            user_obj = dict()
            user_obj['admin_name'] = user.username
            user_obj['admin'] = user.pk
            admin_list.append(user_obj)
        res.update({'data': {
            'admin_list': admin_list
        }})
        res['meta']['code'] = 200
        res['meta']['message'] = '获取成功'

    return JsonResponse(res, safe=False)


@need_login
def test(request):
    res = {
        'meta': {
            'message': '删除地址信息失败',
            'code': 400
        }}

    return JsonResponse(res, safe=False)
