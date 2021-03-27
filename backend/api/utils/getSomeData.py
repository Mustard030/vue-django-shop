from .. import models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
import django.utils.timezone as timezone


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
            'date': str(item.get('year')) + '-' + month,
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

    second_kind_obj_list = [{"name": s, "value": second_kind_dict[s]} for s in second_kind_dict]
    first_kind_obj_list = [{"name": s, "value": first_kind_dict[s]} for s in first_kind_dict]

    return [{"name": "一级分类", "data": first_kind_obj_list},
            {"name": "二级分类", "data": second_kind_obj_list},]


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
            'date': str(item.get('year')) + '-' + month,
            'count': item.get('count')
        })

    order_data_list.sort(key=lambda temp: temp.get('date'))
    return order_data_list
