import json
import os
import uuid
import datetime as dt
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from rest_framework.views import APIView
from .. import models
from django.conf import settings
from ..utils.token import get_token_code
from django.core.files import File
from django.db.models import Q, F
from ..utils.decorator import need_admin


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
