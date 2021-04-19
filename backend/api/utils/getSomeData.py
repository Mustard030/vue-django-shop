import uuid
import random
import time
from .. import models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count
import django.utils.timezone as timezone
from django.db.models import F


def getLastYearRegisteredUser():
    start = datetime.now() - relativedelta(months=12)
    now = datetime.now()
    userYearList = models.MyUserInfo.objects.filter(date_joined__range=(start, now))
    userdata = userYearList.extra(select={'year': 'year(date_joined)', 'month': 'month(date_joined)'}) \
        .values('year', 'month').annotate(count=Count('date_joined')).order_by()
    userdata_list = list()
    for item in userdata:
        month = str(item.get('month')) if item.get('month') > 9 else '0' + str(item.get('month'))
        userdata_list.append({
            'date': str(item.get('year')) + '年' + month + '月',
            'count': item.get('count')
        })

    userdata_list.sort(key=lambda temp: temp.get('date'))
    return userdata_list


def get4DataOfNum():
    this_year = timezone.now().year
    this_month = timezone.now().month
    doneOrderListInThisMonth = models.Orders.objects.filter(pay_status=True, send_status=True, delivery_status=True,
                                                            create_date__year=this_year, create_date__month=this_month)
    doneOrderNumInThisMonth = doneOrderListInThisMonth.count()
    totalSales = 0
    for order in doneOrderListInThisMonth:
        for item_obj in order.orderdetail_set.all():
            totalSales += item_obj.item.price * item_obj.number
    unsendOrderNumInThisMonth = models.Orders.objects.filter(pay_status=True, send_status=False, delivery_status=False,
                                                             create_date__year=this_year,
                                                             create_date__month=this_month).count()
    unreceOrderNumInThisMonth = models.Orders.objects.filter(pay_status=True, send_status=True, delivery_status=False,
                                                             create_date__year=this_year,
                                                             create_date__month=this_month).count()

    return doneOrderNumInThisMonth, totalSales, unsendOrderNumInThisMonth, unreceOrderNumInThisMonth


def getSoldData():
    this_year = timezone.now().year
    this_month = timezone.now().month
    doneOrderListInThisMonth = models.Orders.objects.filter(create_date__year=this_year, create_date__month=this_month)
    second_kind_dict = dict()
    first_kind_dict = dict()
    for order in doneOrderListInThisMonth:
        for item_obj in order.orderdetail_set.all():
            if (sk := item_obj.item.itemClass.name) in second_kind_dict:
                second_kind_dict[sk] += item_obj.number
            else:
                second_kind_dict[sk] = item_obj.number

            if (fk := item_obj.item.itemClass.parent.name) in first_kind_dict:
                first_kind_dict[fk] += item_obj.number
            else:
                first_kind_dict[fk] = item_obj.number

    first_kind_obj_list = [{"name": s, "value": first_kind_dict[s]} for s in first_kind_dict]
    second_kind_obj_list = [{"name": s, "value": second_kind_dict[s]} for s in second_kind_dict]
    first_kind_obj_list = sorted(first_kind_obj_list, key=lambda i: i['value'], reverse=True)[:5]
    second_kind_obj_list = sorted(second_kind_obj_list, key=lambda i: i['value'], reverse=True)[:8]
    # print(first_kind_obj_list)
    # print(second_kind_obj_list)

    return [{"name": "一级分类", "data": first_kind_obj_list},
            {"name": "二级分类", "data": second_kind_obj_list}]


def getOrderData():
    start = datetime.now() - relativedelta(months=12)
    now = datetime.now()
    orderYearList = models.Orders.objects.filter(create_date__range=(start, now))
    order_data = orderYearList.extra(select={'year': 'year(create_date)', 'month': 'month(create_date)'}) \
        .values('year', 'month').annotate(count=Count('create_date')).order_by()
    order_data_list = list()
    for item in order_data:
        month = str(item.get('month')) if item.get('month') > 9 else '0' + str(item.get('month'))
        order_data_list.append({
            'date': str(item.get('year')) + '年' + month + '月',
            'count': item.get('count')
        })

    order_data_list.sort(key=lambda temp: temp.get('date'))
    return order_data_list


def get_a_random_date(s_t=None):
    end_time = datetime.now()
    if s_t:
        start_time = datetime.strptime(s_t, "%Y-%m-%d %H:%M:%S")
    else:
        start_time = datetime.now() + timedelta(days=-365)  # 当前时间减去365天

    a1 = tuple(start_time.timetuple()[0:9])  # 设置开始日期时间元组（2020-04-11 16:30:21）
    a2 = tuple(end_time.timetuple()[0:9])  # 设置结束日期时间元组（2020-04-11 16:33:21）

    start = time.mktime(a1)  # 生成开始时间戳
    end = time.mktime(a2)  # 生成结束时间戳

    # 随机生成日期字符串
    t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
    date_touple = time.localtime(t)  # 将时间戳生成时间元组
    date = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)  # 将时间元组转成格式化字符串（2020-04-11 16:33:21）
    return date


def generate_fake_delivery(order):
    message = "此消息为虚假订单生成的消息"
    for _ in range(random.randint(1, 5)):
        p_time = get_a_random_date(order.create_date)
        models.ProgressInfo.objects.create(order=order, message=message, time=p_time)


def generate_fake_item(order):
    item_list = models.GoodsInfo.objects.filter(reserve__gt=0, usable=True).all()
    choose_item_list = random.sample(list(item_list), random.randint(1, 5))
    for item in choose_item_list:
        item_num = random.randint(1, 10 if item.reserve > 10 else item.reserve)
        models.OrderDetail.objects.create(item=item, number=item_num, order=order)
        item.reserve = F('reserve') - item_num
        item.save()


def generate_fake_order(num, user=None):
    try:
        flag = False
        for i in range(num):
            order_id = uuid.uuid4()
            if user:
                user_obj = models.MyUserInfo.objects.filter(username=user).first()
            else:
                user_list = models.MyUserInfo.objects.filter(is_superuser=False, is_staff=False, is_active=True)
                user_obj = random.choice(user_list)
            delivery_obj = models.DeliveryInfo.objects.get(pk=13)
            random_date = get_a_random_date()

            pay_status = random.choice([True, False])
            send_status = random.choice([True, False]) if pay_status else False
            delivery_status = random.choice([True, False]) if send_status else False

            new_fake_order = models.Orders.objects.create(id=order_id, user=user_obj, deliveryInfo=delivery_obj,
                                                          pay_status=pay_status, send_status=send_status,
                                                          delivery_status=delivery_status,
                                                          create_date=random_date, mod_date=random_date)
            generate_fake_item(new_fake_order)
            if send_status:
                generate_fake_delivery(new_fake_order)
    except Exception as E:
        raise E
    else:
        flag = True
    return flag
